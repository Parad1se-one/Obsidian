#!/usr/bin/env python3
"""Generate visualization plots for DisCoRL CartPole experiment."""

import matplotlib.pyplot as plt
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
fig_width = 12
fig_height = 10

# Create figure with subplots
fig, axes = plt.subplots(2, 2, figsize=(fig_width, fig_height))

# Data from experiment
teacher_training_episodes = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
teacher_avg_rewards = [25.04, 91.82, 141.02, 112.28, 137.88, 153.08, 127.88, 119.92, 166.16, 188.32]

distillation_epochs = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200]
distill_loss = [0.4554, 0.4195, 0.4026, 0.3853, 0.3480, 0.3035, 0.2904, 0.2783, 0.2627, 0.2491]
distill_component = [0.2727, 0.2862, 0.2961, 0.2128, 0.2415, 0.1544, 0.2097, 0.2312, 0.2256, 0.1420]
hard_loss = [0.6567, 0.5886, 0.6560, 0.6242, 0.5934, 0.5640, 0.4629, 0.4752, 0.4225, 0.4350]

# Plot 1: Teacher Training Progress
ax1 = axes[0, 0]
ax1.plot(teacher_training_episodes, teacher_avg_rewards, 'b-o', linewidth=2, markersize=6)
ax1.set_xlabel('Episode', fontsize=11)
ax1.set_ylabel('Average Reward (last 50)', fontsize=11)
ax1.set_title('🏫 Teacher Network Training Progress', fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=500, color='g', linestyle='--', alpha=0.5, label='Target (500)')
ax1.legend()

# Plot 2: Distillation Loss Breakdown
ax2 = axes[0, 1]
ax2.plot(distillation_epochs, distill_loss, 'r-o', linewidth=2, markersize=6, label='Total Loss')
ax2.plot(distillation_epochs, distill_component, 'g--s', linewidth=2, markersize=5, label='Distillation Loss')
ax2.plot(distillation_epochs, hard_loss, 'b-.^', linewidth=2, markersize=5, label='Hard Label Loss')
ax2.set_xlabel('Epoch', fontsize=11)
ax2.set_ylabel('Loss', fontsize=11)
ax2.set_title('🎓 Knowledge Distillation Training', fontsize=12, fontweight='bold')
ax2.legend(loc='upper right')
ax2.grid(True, alpha=0.3)

# Plot 3: Model Comparison - Performance
ax3 = axes[1, 0]
models = ['Teacher\n(101,506 params)', 'Student\n(4,610 params)']
mean_rewards = [19.45, 67.45]
std_rewards = [2.33, 33.15]
colors = ['#2E86AB', '#A23B72']
bars = ax3.bar(models, mean_rewards, yerr=std_rewards, capsize=8, color=colors, alpha=0.8)
ax3.set_ylabel('Mean Reward ± Std', fontsize=11)
ax3.set_title('📊 Model Performance Comparison', fontsize=12, fontweight='bold')
ax3.axhline(y=500, color='g', linestyle='--', alpha=0.5, label='CartPole-v1 Max')
for i, (bar, val) in enumerate(zip(bars, mean_rewards)):
    ax3.text(i, val + 5, f'{val:.1f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
ax3.legend()

# Plot 4: Model Size Comparison
ax4 = axes[1, 1]
param_counts = [101506, 4610]
reduction = 95.5
wedges, texts, autotexts = ax4.pie(param_counts, labels=['Teacher', 'Student'], 
                                    autopct='%1.1f%%', colors=['#2E86AB', '#A23B72'],
                                    explode=(0, 0.1))
ax4.set_title(f'💾 Model Size Comparison\n(Student: {reduction}% smaller)', fontsize=12, fontweight='bold')

plt.suptitle('DisCoRL CartPole Knowledge Distillation Experiment Results', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()

# Save plot
plt.savefig('research/experiments/discorl-cartpole-results.png', dpi=150, bbox_inches='tight')
print("✅ Plot saved to research/experiments/discorl-cartpole-results.png")
plt.close()
