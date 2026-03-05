#!/usr/bin/env python3
"""
自优化系统 v1.0 - 持续改进 Agent 性能

小虾 🦐 | 2026-03-06
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SelfOptimizer:
    """自优化器"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace) if workspace else Path('/home/openclaw/.openclaw/workspace/obsidian-repo')
        self.improvement_log = self.workspace / 'projects' / 'research-agent-system' / 'improvements.json'
        self.strategy_file = self.workspace / 'projects' / 'research-agent-system' / 'strategies.json'
        
        self.improvements = self._load_json(self.improvement_log, {'history': []})
        self.strategies = self._load_json(self.strategy_file, self._default_strategies())
    
    def _load_json(self, path: Path, default: Dict) -> Dict:
        """加载 JSON 文件"""
        if path.exists():
            with open(path, encoding='utf-8') as f:
                return json.load(f)
        return default
    
    def _default_strategies(self) -> Dict:
        """默认策略"""
        return {
            'literature': {
                'search_keywords': ['reinforcement learning', 'knowledge distillation'],
                'min_papers': 5,
                'note_template': 'standard',
                'retry_on_failure': True,
                'max_retries': 3
            },
            'research': {
                'min_research_questions': 2,
                'include_feasibility': True,
                'timeline_weeks': 8,
                'retry_on_failure': True,
                'max_retries': 2
            },
            'code': {
                'prefer_pure_python': True,
                'add_comments': True,
                'include_tests': True,
                'retry_on_failure': True,
                'max_retries': 3
            },
            'analysis': {
                'include_statistics': True,
                'generate_figures': True,
                'min_word_count': 800,
                'retry_on_failure': True,
                'max_retries': 2
            },
            'writing': {
                'include_all_sections': True,
                'citation_style': 'apa',
                'min_word_count': 3000,
                'retry_on_failure': True,
                'max_retries': 2
            }
        }
    
    def record_improvement(self, agent_type: str, validation_result: Dict):
        """记录改进"""
        improvement = {
            'timestamp': datetime.now().isoformat(),
            'agent': agent_type,
            'score': validation_result.get('score', 0),
            'passed': validation_result.get('passed', False),
            'failures': validation_result.get('failures', []),
            'recommendations': validation_result.get('recommendations', [])
        }
        
        self.improvements['history'].append(improvement)
        
        # 保存
        with open(self.improvement_log, 'w', encoding='utf-8') as f:
            json.dump(self.improvements, f, indent=2, ensure_ascii=False)
        
        # 分析并更新策略
        self._analyze_and_update(agent_type, validation_result)
        
        print(f"📝 改进记录已保存")
    
    def _analyze_and_update(self, agent_type: str, validation_result: Dict):
        """分析失败并更新策略"""
        if validation_result.get('passed', False):
            print(f"✅ {agent_type} 通过验证，无需调整")
            return
        
        print(f"🔧 分析 {agent_type} 失败原因...")
        
        failures = validation_result.get('failures', [])
        recommendations = validation_result.get('recommendations', [])
        
        # 根据失败原因调整策略
        if agent_type == 'literature':
            for failure in failures:
                metric = failure.get('metric', '')
                if '文件' in failure.get('reason', '') or '数量' in metric:
                    # 增加最少论文数量
                    self.strategies['literature']['min_papers'] += 1
                    print(f"  → 增加最少论文数量：{self.strategies['literature']['min_papers']}")
                
                if '字数' in failure.get('reason', ''):
                    # 切换为详细模板
                    self.strategies['literature']['note_template'] = 'detailed'
                    print(f"  → 切换为详细笔记模板")
        
        elif agent_type == 'research':
            for failure in failures:
                if '可行性' in failure.get('reason', ''):
                    # 增加可行性评估权重
                    self.strategies['research']['include_feasibility'] = True
                    print(f"  → 强制包含可行性评估")
        
        elif agent_type == 'code':
            for failure in failures:
                if '运行' in failure.get('reason', ''):
                    # 优先使用纯 Python
                    self.strategies['code']['prefer_pure_python'] = True
                    print(f"  → 优先使用纯 Python 实现")
                
                if '质量' in failure.get('reason', ''):
                    # 强制添加注释
                    self.strategies['code']['add_comments'] = True
                    print(f"  → 强制添加代码注释")
        
        elif agent_type == 'analysis':
            for failure in failures:
                if '统计' in failure.get('reason', ''):
                    # 强制包含统计检验
                    self.strategies['analysis']['include_statistics'] = True
                    print(f"  → 强制包含统计检验")
        
        elif agent_type == 'writing':
            for failure in failures:
                if '章节' in failure.get('reason', ''):
                    # 强制包含所有章节
                    self.strategies['writing']['include_all_sections'] = True
                    print(f"  → 强制包含所有章节")
        
        # 保存更新后的策略
        with open(self.strategy_file, 'w', encoding='utf-8') as f:
            json.dump(self.strategies, f, indent=2, ensure_ascii=False)
        
        print(f"✅ 策略已更新")
    
    def get_strategy(self, agent_type: str) -> Dict:
        """获取当前策略"""
        return self.strategies.get(agent_type, {})
    
    def generate_report(self) -> Dict:
        """生成改进报告"""
        history = self.improvements.get('history', [])
        
        if not history:
            return {'message': '无改进记录'}
        
        # 按 Agent 分组统计
        agent_stats = {}
        for record in history:
            agent = record['agent']
            if agent not in agent_stats:
                agent_stats[agent] = {
                    'total': 0,
                    'passed': 0,
                    'scores': [],
                    'common_failures': {}
                }
            
            agent_stats[agent]['total'] += 1
            if record['passed']:
                agent_stats[agent]['passed'] += 1
            agent_stats[agent]['scores'].append(record['score'])
            
            # 统计常见失败
            for failure in record.get('failures', []):
                metric = failure.get('metric', 'Unknown')
                agent_stats[agent]['common_failures'][metric] = \
                    agent_stats[agent]['common_failures'].get(metric, 0) + 1
        
        # 计算通过率
        for agent in agent_stats:
            stats = agent_stats[agent]
            stats['pass_rate'] = stats['passed'] / stats['total'] if stats['total'] > 0 else 0
            stats['avg_score'] = sum(stats['scores']) / len(stats['scores']) if stats['scores'] else 0
        
        return {
            'generated_at': datetime.now().isoformat(),
            'total_records': len(history),
            'agent_stats': agent_stats
        }


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='自优化系统')
    parser.add_argument('action', choices=['record', 'report', 'strategy'],
                       help='操作类型')
    parser.add_argument('--agent', '-a', choices=['literature', 'research', 'code', 'analysis', 'writing'],
                       help='Agent 类型')
    parser.add_argument('--result', '-r', help='验证结果 JSON 文件')
    parser.add_argument('--workspace', '-w', default='/home/openclaw/.openclaw/workspace/obsidian-repo',
                       help='工作空间路径')
    
    args = parser.parse_args()
    
    optimizer = SelfOptimizer(args.workspace)
    
    if args.action == 'record':
        if not args.agent or not args.result:
            print("错误：record 操作需要 --agent 和 --result")
            return
        
        with open(args.result, encoding='utf-8') as f:
            validation_result = json.load(f)
        
        optimizer.record_improvement(args.agent, validation_result)
    
    elif args.action == 'report':
        report = optimizer.generate_report()
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    elif args.action == 'strategy':
        if not args.agent:
            print("错误：strategy 操作需要 --agent")
            return
        
        strategy = optimizer.get_strategy(args.agent)
        print(f"{args.agent} 当前策略:")
        print(json.dumps(strategy, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
