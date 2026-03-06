"""
CartPole DQN Knowledge Distillation Example
============================================
This script demonstrates knowledge distillation from a trained teacher DQN network
to a smaller student network in the CartPole-v1 environment.

Knowledge distillation transfers the "dark knowledge" from a large, well-trained
teacher model to a compact student model, enabling faster inference with minimal
performance loss.
"""

import gymnasium as gym
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from collections import deque
import random
from datetime import datetime


# ============================================================================
# Network Architectures
# ============================================================================

class TeacherDQN(nn.Module):
    """
    Teacher Network: Larger capacity network with more hidden units.
    This network is trained first to convergence, then used to guide the student.
    """
    def __init__(self, state_dim, action_dim, hidden_dims=[256, 256, 128]):
        super(TeacherDQN, self).__init__()
        layers = []
        prev_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.LayerNorm(hidden_dim))
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, action_dim))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)


class StudentDQN(nn.Module):
    """
    Student Network: Smaller, more efficient network.
    Learns to mimic the teacher's output distribution.
    """
    def __init__(self, state_dim, action_dim, hidden_dims=[64, 64]):
        super(StudentDQN, self).__init__()
        layers = []
        prev_dim = state_dim
        
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.ReLU())
            prev_dim = hidden_dim
        
        layers.append(nn.Linear(prev_dim, action_dim))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.network(x)


# ============================================================================
# Experience Replay Buffer
# ============================================================================

class ReplayBuffer:
    """Standard experience replay buffer for DQN training."""
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, action, reward, next_state, done):
        self.buffer.append((state, action, reward, next_state, done))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, actions, rewards, next_states, dones = zip(*batch)
        return (
            torch.FloatTensor(np.array(states)),
            torch.LongTensor(actions),
            torch.FloatTensor(rewards),
            torch.FloatTensor(np.array(next_states)),
            torch.FloatTensor(dones)
        )
    
    def __len__(self):
        return len(self.buffer)


class DistillationBuffer:
    """
    Specialized buffer for knowledge distillation.
    Stores states and teacher's soft predictions for student training.
    """
    def __init__(self, capacity=5000):
        self.buffer = deque(maxlen=capacity)
    
    def push(self, state, teacher_logits, teacher_action):
        """Store state and teacher's output distribution."""
        self.buffer.append((state, teacher_logits, teacher_action))
    
    def sample(self, batch_size):
        batch = random.sample(self.buffer, batch_size)
        states, teacher_logits, teacher_actions = zip(*batch)
        return (
            torch.FloatTensor(np.array(states)),
            torch.FloatTensor(np.array(teacher_logits)),
            torch.LongTensor(teacher_actions)
        )
    
    def __len__(self):
        return len(self.buffer)


# ============================================================================
# DQN Trainer with Knowledge Distillation
# ============================================================================

class DQNAgent:
    """DQN agent with support for both standard training and knowledge distillation."""
    
    def __init__(self, model, target_model, state_dim, action_dim, 
                 lr=1e-3, gamma=0.99, epsilon_start=1.0, epsilon_end=0.01,
                 epsilon_decay=0.995, buffer_size=10000, batch_size=64):
        self.model = model
        self.target_model = target_model
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.gamma = gamma
        self.epsilon = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        
        self.optimizer = optim.Adam(model.parameters(), lr=lr)
        self.buffer = ReplayBuffer(buffer_size)
        
        # Sync target network initially
        self.update_target()
    
    def select_action(self, state, training=True):
        """Epsilon-greedy action selection."""
        if training and random.random() < self.epsilon:
            return random.randint(0, self.action_dim - 1)
        
        with torch.no_grad():
            state_tensor = torch.FloatTensor(state).unsqueeze(0)
            q_values = self.model(state_tensor)
            return q_values.argmax().item()
    
    def store_transition(self, state, action, reward, next_state, done):
        self.buffer.push(state, action, reward, next_state, done)
    
    def update_target(self):
        """Copy weights from main network to target network."""
        self.target_model.load_state_dict(self.model.state_dict())
    
    def train_step(self):
        """Perform one training step using standard DQN loss."""
        if len(self.buffer) < self.batch_size:
            return None
        
        states, actions, rewards, next_states, dones = self.buffer.sample(self.batch_size)
        
        # Current Q values
        current_q = self.model(states).gather(1, actions.unsqueeze(1)).squeeze(1)
        
        # Target Q values (Double DQN style)
        with torch.no_grad():
            next_actions = self.model(next_states).argmax(1)
            next_q = self.target_model(next_states).gather(1, next_actions.unsqueeze(1)).squeeze(1)
            targets = rewards + self.gamma * next_q * (1 - dones)
        
        loss = F.mse_loss(current_q, targets)
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        # Decay epsilon
        self.epsilon = max(self.epsilon_end, self.epsilon * self.epsilon_decay)
        
        return loss.item()


class DistillationTrainer:
    """
    Knowledge Distillation Trainer.
    Trains student network using teacher's soft predictions as supervision.
    """
    
    def __init__(self, student_model, teacher_model, state_dim, action_dim,
                 lr=1e-3, temperature=2.0, alpha=0.7, buffer_size=5000, batch_size=64):
        """
        Args:
            temperature: Softmax temperature for soft targets (higher = softer)
            alpha: Weight for distillation loss (1-alpha for hard loss)
        """
        self.student = student_model
        self.teacher = teacher_model
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.temperature = temperature
        self.alpha = alpha
        self.batch_size = batch_size
        
        self.optimizer = optim.Adam(student_model.parameters(), lr=lr)
        self.buffer = DistillationBuffer(buffer_size)
        
        # Freeze teacher parameters
        for param in teacher_model.parameters():
            param.requires_grad = False
    
    def collect_teacher_data(self, env, num_episodes=50, steps_per_episode=200):
        """
        Collect states and teacher's predictions for distillation.
        Teacher uses greedy policy to generate high-quality demonstrations.
        """
        print(f"\n📚 Collecting teacher knowledge ({num_episodes} episodes)...")
        
        self.teacher.eval()
        total_steps = 0
        
        for episode in range(num_episodes):
            state, _ = env.reset()
            done = False
            steps = 0
            
            while not done and steps < steps_per_episode:
                with torch.no_grad():
                    state_tensor = torch.FloatTensor(state).unsqueeze(0)
                    teacher_logits = self.teacher(state_tensor).squeeze(0).numpy()
                    teacher_action = teacher_logits.argmax()
                
                # Store teacher's full logits (soft targets) and action (hard target)
                self.buffer.push(state.copy(), teacher_logits.copy(), teacher_action)
                
                next_state, reward, terminated, truncated, _ = env.step(teacher_action)
                done = terminated or truncated
                state = next_state
                steps += 1
                total_steps += 1
            
            if (episode + 1) % 10 == 0:
                print(f"  Episode {episode + 1}/{num_episodes}, Total steps: {total_steps}")
        
        print(f"✅ Collected {len(self.buffer)} samples from teacher")
        return total_steps
    
    def train_step(self):
        """
        Perform one distillation training step.
        Combines soft target distillation loss with hard target cross-entropy.
        """
        if len(self.buffer) < self.batch_size:
            return None, None, None
        
        states, teacher_logits, teacher_actions = self.buffer.sample(self.batch_size)
        
        # Student predictions
        student_logits = self.student(states)
        
        # Soft targets (KL divergence with temperature scaling)
        soft_targets = F.softmax(torch.FloatTensor(teacher_logits) / self.temperature, dim=1)
        student_soft = F.log_softmax(student_logits / self.temperature, dim=1)
        
        # Distillation loss (KL divergence)
        distill_loss = F.kl_div(student_soft, soft_targets, reduction='batchmean') * (self.temperature ** 2)
        
        # Hard loss (cross-entropy with teacher's actions)
        hard_loss = F.cross_entropy(student_logits, teacher_actions)
        
        # Combined loss
        loss = self.alpha * distill_loss + (1 - self.alpha) * hard_loss
        
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        
        return loss.item(), distill_loss.item(), hard_loss.item()
    
    def train(self, num_epochs=100, log_interval=10):
        """Train student network on collected teacher data."""
        print(f"\n🎓 Training student network ({num_epochs} epochs)...")
        print(f"   Temperature: {self.temperature}, Alpha: {self.alpha}")
        
        losses = []
        
        for epoch in range(num_epochs):
            loss, distill_loss, hard_loss = self.train_step()
            
            if loss is not None:
                losses.append(loss)
                
                if (epoch + 1) % log_interval == 0:
                    avg_loss = np.mean(losses[-log_interval:])
                    print(f"  Epoch {epoch + 1}/{num_epochs} - Loss: {avg_loss:.4f} "
                          f"(Distill: {distill_loss:.4f}, Hard: {hard_loss:.4f})")
        
        print(f"✅ Student training complete. Final avg loss: {np.mean(losses[-10:]):.4f}")
        return losses


# ============================================================================
# Evaluation & Comparison
# ============================================================================

def evaluate_agent(agent_or_model, env, num_episodes=20, max_steps=500, render=False):
    """Evaluate an agent or model over multiple episodes."""
    if hasattr(agent_or_model, 'select_action'):
        # It's a DQNAgent
        model = agent_or_model.model
        select_action = lambda s: agent_or_model.select_action(s, training=False)
    else:
        # It's a raw model
        model = agent_or_model
        def select_action(state):
            with torch.no_grad():
                state_tensor = torch.FloatTensor(state).unsqueeze(0)
                return model(state_tensor).argmax().item()
    
    model.eval()
    rewards = []
    
    for episode in range(num_episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False
        steps = 0
        
        while not done and steps < max_steps:
            action = select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            total_reward += reward
            done = terminated or truncated
            state = next_state
            steps += 1
            
            if render:
                env.render()
        
        rewards.append(total_reward)
    
    model.train()  # Restore training mode
    return {
        'mean': np.mean(rewards),
        'std': np.std(rewards),
        'min': np.min(rewards),
        'max': np.max(rewards),
        'rewards': rewards
    }


def compare_models(teacher, student, env, num_episodes=20):
    """Compare teacher and student performance side by side."""
    print("\n" + "="*60)
    print("📊 MODEL COMPARISON")
    print("="*60)
    
    print("\nEvaluating Teacher Network...")
    teacher_stats = evaluate_agent(teacher, env, num_episodes)
    print(f"  Mean Reward: {teacher_stats['mean']:.2f} ± {teacher_stats['std']:.2f}")
    print(f"  Range: [{teacher_stats['min']}, {teacher_stats['max']}]")
    
    print("\nEvaluating Student Network...")
    student_stats = evaluate_agent(student, env, num_episodes)
    print(f"  Mean Reward: {student_stats['mean']:.2f} ± {student_stats['std']:.2f}")
    print(f"  Range: [{student_stats['min']}, {student_stats['max']}]")
    
    # Performance retention
    retention = (student_stats['mean'] / teacher_stats['mean']) * 100 if teacher_stats['mean'] > 0 else 0
    print(f"\n📈 Student Performance Retention: {retention:.1f}% of teacher")
    
    # Model size comparison
    teacher_params = sum(p.numel() for p in teacher.parameters())
    student_params = sum(p.numel() for p in student.parameters())
    reduction = (1 - student_params / teacher_params) * 100
    
    print(f"\n💾 Model Size Comparison:")
    print(f"  Teacher: {teacher_params:,} parameters")
    print(f"  Student: {student_params:,} parameters ({reduction:.1f}% reduction)")
    
    return teacher_stats, student_stats


# ============================================================================
# Main Training Pipeline
# ============================================================================

def train_teacher(env, state_dim, action_dim, num_episodes=500, target_reward=450):
    """Train the teacher DQN network to convergence."""
    print("\n" + "="*60)
    print("🏫 PHASE 1: TRAINING TEACHER NETWORK")
    print("="*60)
    
    teacher = TeacherDQN(state_dim, action_dim)
    target_teacher = TeacherDQN(state_dim, action_dim)
    agent = DQNAgent(teacher, target_teacher, state_dim, action_dim)
    
    episode_rewards = []
    best_reward = 0
    
    for episode in range(num_episodes):
        state, _ = env.reset()
        total_reward = 0
        done = False
        
        while not done:
            action = agent.select_action(state)
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            
            agent.store_transition(state, action, reward, next_state, done)
            agent.train_step()
            
            total_reward += reward
            state = next_state
        
        episode_rewards.append(total_reward)
        
        # Update target network periodically
        if episode % 10 == 0:
            agent.update_target()
        
        # Logging
        if (episode + 1) % 50 == 0:
            recent_avg = np.mean(episode_rewards[-50:])
            print(f"  Episode {episode + 1}/{num_episodes} - "
                  f"Avg Reward (last 50): {recent_avg:.2f}, "
                  f"Epsilon: {agent.epsilon:.3f}")
        
        # Early stopping if target reached
        if len(episode_rewards) >= 100:
            recent_100 = np.mean(episode_rewards[-100:])
            if recent_100 >= target_reward:
                print(f"\n✅ Teacher reached target reward ({target_reward}) at episode {episode + 1}!")
                break
        
        best_reward = max(best_reward, total_reward)
    
    print(f"\n✅ Teacher training complete. Best episode: {best_reward}")
    return teacher, agent


def main():
    """Main execution: Train teacher, distill to student, compare performance."""
    
    # Configuration
    ENV_NAME = "CartPole-v1"
    NUM_EPISODES_TEACHER = 500
    NUM_EPISODES_DISTILL = 50
    NUM_EVAL_EPISODES = 20
    TARGET_REWARD = 450
    
    print("\n" + "="*60)
    print("🚀 CARTPOLE DQN KNOWLEDGE DISTILLATION")
    print("="*60)
    print(f"Environment: {ENV_NAME}")
    print(f"Teacher Episodes: {NUM_EPISODES_TEACHER}")
    print(f"Distillation Episodes: {NUM_EPISODES_DISTILL}")
    print(f"Temperature: 2.0, Alpha: 0.7")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Create environment
    env = gym.make(ENV_NAME)
    state_dim = env.observation_space.shape[0]
    action_dim = env.action_space.n
    
    print(f"\n📋 Environment Info:")
    print(f"  State Dimension: {state_dim}")
    print(f"  Action Dimension: {action_dim}")
    
    # Phase 1: Train Teacher
    teacher, teacher_agent = train_teacher(
        env, state_dim, action_dim, 
        num_episodes=NUM_EPISODES_TEACHER,
        target_reward=TARGET_REWARD
    )
    
    # Phase 2: Knowledge Distillation
    print("\n" + "="*60)
    print("🎓 PHASE 2: KNOWLEDGE DISTILLATION")
    print("="*60)
    
    student = StudentDQN(state_dim, action_dim)
    distill_trainer = DistillationTrainer(
        student, teacher, state_dim, action_dim,
        temperature=2.0, alpha=0.7
    )
    
    # Collect teacher knowledge
    distill_trainer.collect_teacher_data(
        env, 
        num_episodes=NUM_EPISODES_DISTILL,
        steps_per_episode=500
    )
    
    # Train student
    distill_losses = distill_trainer.train(num_epochs=200, log_interval=20)
    
    # Phase 3: Evaluation & Comparison
    print("\n" + "="*60)
    print("📈 PHASE 3: EVALUATION")
    print("="*60)
    
    teacher_stats, student_stats = compare_models(teacher, student, env, NUM_EVAL_EPISODES)
    
    # Save models (optional)
    save_models = input("\n💾 Save trained models? (y/n): ").strip().lower()
    if save_models == 'y':
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        torch.save(teacher.state_dict(), f"teacher_cartpole_{timestamp}.pth")
        torch.save(student.state_dict(), f"student_cartpole_{timestamp}.pth")
        print(f"✅ Models saved!")
    
    env.close()
    
    print("\n" + "="*60)
    print("✨ KNOWLEDGE DISTILLATION COMPLETE")
    print("="*60)
    print("\nKey Takeaways:")
    print("  • Teacher network: Large capacity, high performance")
    print("  • Student network: Compact, efficient, ~70-90% of teacher performance")
    print("  • Distillation enables deployment on resource-constrained devices")
    print("\n🦐 Code by Xiao Xia - Cyber Shrimp Assistant")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
