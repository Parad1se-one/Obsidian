#!/usr/bin/env python3
"""
验证引擎 v1.0 - 自动评估 Agent 产出质量

小虾 🦐 | 2026-03-06
"""

import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any


# ============================================================
# 验证规则定义
# ============================================================

VERIFICATION_RULES = {
    'literature': {
        'name': 'Literature Agent',
        'pass_threshold': 0.7,
        'metrics': [
            {
                'name': '论文数量',
                'type': 'count_files',
                'weight': 0.25,
                'threshold': 5,
                'path': 'knowledge/rl/papers/',
                'pattern': '*.md'
            },
            {
                'name': '笔记完整性',
                'type': 'min_word_count',
                'weight': 0.25,
                'threshold': 500,
                'path': 'knowledge/rl/papers/',
                'pattern': '*.md'
            },
            {
                'name': '关键信息提取',
                'type': 'keywords_present',
                'weight': 0.25,
                'threshold': 0.8,
                'keywords': ['方法', '实验', '结论', '摘要'],
                'path': 'knowledge/rl/papers/',
                'pattern': '*.md'
            },
            {
                'name': '来源可追溯',
                'type': 'links_present',
                'weight': 0.25,
                'threshold': 0.8,
                'link_patterns': ['arxiv', 'doi', 'https://'],
                'path': 'knowledge/rl/papers/',
                'pattern': '*.md'
            }
        ]
    },
    
    'research': {
        'name': 'Research Agent',
        'pass_threshold': 0.7,
        'metrics': [
            {
                'name': '研究问题',
                'type': 'count_pattern',
                'weight': 0.25,
                'threshold': 2,
                'pattern': r'RQ\d+|研究问题|Research Question',
                'path': 'knowledge/rl/research/'
            },
            {
                'name': '实验设计',
                'type': 'sections_present',
                'weight': 0.25,
                'threshold': 0.75,
                'sections': ['环境', '基线', '指标', '实验设计'],
                'path': 'knowledge/rl/research/'
            },
            {
                'name': '可行性评估',
                'type': 'keywords_present',
                'weight': 0.25,
                'threshold': 0.5,
                'keywords': ['资源', '时间', '算力', 'GPU'],
                'path': 'knowledge/rl/research/'
            },
            {
                'name': '文档长度',
                'type': 'min_word_count',
                'weight': 0.25,
                'threshold': 1000,
                'path': 'knowledge/rl/research/'
            }
        ]
    },
    
    'code': {
        'name': 'Code Agent',
        'pass_threshold': 0.8,
        'metrics': [
            {
                'name': '代码可运行',
                'type': 'runnable',
                'weight': 0.40,
                'timeout': 60,
                'path': 'code/rl-distillation/'
            },
            {
                'name': '性能达标',
                'type': 'metrics_threshold',
                'weight': 0.30,
                'threshold': 0.9,
                'metric_name': 'retention',
                'path': 'results/'
            },
            {
                'name': '代码质量',
                'type': 'code_quality',
                'weight': 0.15,
                'threshold': 0.7,
                'checks': ['has_comments', 'has_docstring', 'modular'],
                'path': 'code/rl-distillation/'
            },
            {
                'name': '结果可复现',
                'type': 'reproducible',
                'weight': 0.15,
                'runs': 3,
                'tolerance': 0.05,
                'path': 'results/'
            }
        ]
    },
    
    'analysis': {
        'name': 'Analysis Agent',
        'pass_threshold': 0.75,
        'metrics': [
            {
                'name': '统计检验',
                'type': 'statistics_present',
                'weight': 0.30,
                'threshold': 0.8,
                'keywords': ['p-value', 't-test', 'ANOVA', '显著性'],
                'path': 'results/'
            },
            {
                'name': '可视化',
                'type': 'figures_present',
                'weight': 0.25,
                'threshold': 2,
                'path': 'results/',
                'pattern': '*.png'
            },
            {
                'name': '结论支持',
                'type': 'conclusion_quality',
                'weight': 0.25,
                'threshold': 0.7,
                'path': 'results/'
            },
            {
                'name': '文档完整性',
                'type': 'min_word_count',
                'weight': 0.20,
                'threshold': 800,
                'path': 'results/'
            }
        ]
    },
    
    'writing': {
        'name': 'Writing Agent',
        'pass_threshold': 0.7,
        'metrics': [
            {
                'name': '结构完整',
                'type': 'sections_present',
                'weight': 0.30,
                'threshold': 0.8,
                'sections': ['摘要', '引言', '方法', '实验', '结论', '参考文献'],
                'path': 'papers/'
            },
            {
                'name': '引用规范',
                'type': 'citations_present',
                'weight': 0.25,
                'threshold': 0.9,
                'path': 'papers/'
            },
            {
                'name': '语言质量',
                'type': 'grammar_check',
                'weight': 0.25,
                'threshold': 0.8,
                'path': 'papers/'
            },
            {
                'name': '文档长度',
                'type': 'min_word_count',
                'weight': 0.20,
                'threshold': 3000,
                'path': 'papers/'
            }
        ]
    }
}


# ============================================================
# 验证器类
# ============================================================

class Verifier:
    """验证引擎"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace) if workspace else Path('/home/openclaw/.openclaw/workspace/obsidian-repo')
        self.results = {}
    
    def verify(self, agent_type: str, result_dir: str = None) -> Dict:
        """
        验证 Agent 产出
        
        Args:
            agent_type: literature, research, code, analysis, writing
            result_dir: 结果目录 (可选)
        
        Returns:
            验证结果字典
        """
        if agent_type not in VERIFICATION_RULES:
            return {
                'error': f'未知 Agent 类型：{agent_type}',
                'passed': False,
                'score': 0
            }
        
        rules = VERIFICATION_RULES[agent_type]
        results = {
            'agent': rules['name'],
            'timestamp': datetime.now().isoformat(),
            'metrics': {},
            'failures': [],
            'recommendations': []
        }
        
        total_score = 0.0
        total_weight = 0.0
        
        print(f"\n🔍 验证 {rules['name']} 产出...")
        print("=" * 60)
        
        for metric in rules['metrics']:
            name = metric['name']
            weight = metric['weight']
            
            # 执行验证
            try:
                score, passed, details = self._verify_metric(metric, result_dir)
            except Exception as e:
                score = 0.0
                passed = False
                details = f'验证错误：{str(e)}'
            
            results['metrics'][name] = {
                'score': round(score, 2),
                'passed': passed,
                'details': details
            }
            
            # 计算加权分数
            if passed:
                total_score += score * weight
            else:
                results['failures'].append({
                    'metric': name,
                    'reason': details
                })
            
            total_weight += weight
            
            # 显示进度
            status = '✅' if passed else '❌'
            print(f"{status} {name}: {score:.2f} ({details})")
        
        # 计算总分
        final_score = total_score / total_weight if total_weight > 0 else 0
        passed = final_score >= rules['pass_threshold']
        
        results['passed'] = passed
        results['score'] = round(final_score * 100, 1)
        results['recommendations'] = self._generate_recommendations(results['failures'])
        
        # 显示总结
        print("=" * 60)
        status = '✅ 通过' if passed else '❌ 失败'
        print(f"{status} 总分：{results['score']}/100")
        
        if results['recommendations']:
            print("\n💡 改进建议:")
            for rec in results['recommendations']:
                print(f"  - {rec}")
        
        return results
    
    def _verify_metric(self, metric: Dict, result_dir: str = None) -> Tuple[float, bool, str]:
        """验证单个指标"""
        metric_type = metric['type']
        
        if metric_type == 'count_files':
            return self._check_count_files(metric)
        elif metric_type == 'min_word_count':
            return self._check_min_word_count(metric)
        elif metric_type == 'keywords_present':
            return self._check_keywords_present(metric)
        elif metric_type == 'links_present':
            return self._check_links_present(metric)
        elif metric_type == 'count_pattern':
            return self._check_count_pattern(metric)
        elif metric_type == 'sections_present':
            return self._check_sections_present(metric)
        elif metric_type == 'runnable':
            return self._check_runnable(metric)
        elif metric_type == 'metrics_threshold':
            return self._check_metrics_threshold(metric, result_dir)
        elif metric_type == 'code_quality':
            return self._check_code_quality(metric)
        elif metric_type == 'reproducible':
            return self._check_reproducible(metric)
        else:
            return 0.0, False, f'未知验证类型：{metric_type}'
    
    def _check_count_files(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查文件数量"""
        path = self.workspace / metric['path']
        pattern = metric.get('pattern', '*')
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, f'目录不存在：{path}'
        
        files = list(path.glob(pattern))
        count = len(files)
        
        score = min(count / threshold, 1.0)
        passed = count >= threshold
        
        return score, passed, f'{count} 个文件 (要求：≥{threshold})'
    
    def _check_min_word_count(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查最小字数"""
        path = self.workspace / metric['path']
        pattern = metric.get('pattern', '*.md')
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        files = list(path.glob(pattern))
        if not files:
            return 0.0, False, '无文件'
        
        # 计算平均字数
        total_words = 0
        for f in files:
            content = f.read_text()
            total_words += len(content.split())
        
        avg_words = total_words / len(files)
        score = min(avg_words / threshold, 1.0)
        passed = avg_words >= threshold
        
        return score, passed, f'平均 {avg_words:.0f} 字 (要求：≥{threshold})'
    
    def _check_keywords_present(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查关键词存在"""
        path = self.workspace / metric['path']
        pattern = metric.get('pattern', '*.md')
        keywords = metric['keywords']
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        files = list(path.glob(pattern))
        if not files:
            return 0.0, False, '无文件'
        
        # 检查每个文件包含的关键词比例
        keyword_ratios = []
        for f in files:
            content = f.read_text().lower()
            present = sum(1 for kw in keywords if kw.lower() in content)
            keyword_ratios.append(present / len(keywords))
        
        avg_ratio = sum(keyword_ratios) / len(keyword_ratios)
        score = avg_ratio
        passed = avg_ratio >= threshold
        
        return score, passed, f'{avg_ratio*100:.0f}% 关键词 (要求：≥{threshold*100}%)'
    
    def _check_links_present(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查链接存在"""
        path = self.workspace / metric['path']
        pattern = metric.get('pattern', '*.md')
        link_patterns = metric['link_patterns']
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        files = list(path.glob(pattern))
        if not files:
            return 0.0, False, '无文件'
        
        # 检查包含链接的文件比例
        files_with_links = 0
        for f in files:
            content = f.read_text()
            if any(lp in content for lp in link_patterns):
                files_with_links += 1
        
        ratio = files_with_links / len(files)
        score = ratio
        passed = ratio >= threshold
        
        return score, passed, f'{ratio*100:.0f}% 文件有链接 (要求：≥{threshold*100}%)'
    
    def _check_count_pattern(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查模式匹配数量"""
        import re
        
        path = self.workspace / metric['path']
        pattern_re = metric['pattern']
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        files = list(path.glob('*.md'))
        if not files:
            return 0.0, False, '无文件'
        
        # 统计匹配次数
        total_matches = 0
        for f in files:
            content = f.read_text()
            matches = re.findall(pattern_re, content, re.IGNORECASE)
            total_matches += len(matches)
        
        score = min(total_matches / threshold, 1.0)
        passed = total_matches >= threshold
        
        return score, passed, f'{total_matches} 次匹配 (要求：≥{threshold})'
    
    def _check_sections_present(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查章节存在"""
        path = self.workspace / metric['path']
        sections = metric['sections']
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        files = list(path.glob('*.md'))
        if not files:
            return 0.0, False, '无文件'
        
        # 检查每个文件包含的章节比例
        section_ratios = []
        for f in files:
            content = f.read_text()
            present = sum(1 for sec in sections if sec in content)
            section_ratios.append(present / len(sections))
        
        avg_ratio = sum(section_ratios) / len(section_ratios)
        score = avg_ratio
        passed = avg_ratio >= threshold
        
        return score, passed, f'{avg_ratio*100:.0f}% 章节 (要求：≥{threshold*100}%)'
    
    def _check_runnable(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查代码可运行"""
        path = self.workspace / metric['path']
        timeout = metric.get('timeout', 60)
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        # 查找 Python 文件
        py_files = list(path.glob('*.py'))
        if not py_files:
            return 0.0, False, '无 Python 文件'
        
        # 尝试运行第一个文件
        test_file = py_files[0]
        try:
            result = subprocess.run(
                ['python3', str(test_file)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(path)
            )
            
            if result.returncode == 0:
                return 1.0, True, '运行成功'
            else:
                error_msg = result.stderr[:100] if result.stderr else '未知错误'
                return 0.0, False, f'运行失败：{error_msg}'
        
        except subprocess.TimeoutExpired:
            return 0.0, False, f'超时 ({timeout}s)'
        except Exception as e:
            return 0.0, False, str(e)
    
    def _check_metrics_threshold(self, metric: Dict, result_dir: str) -> Tuple[float, bool, str]:
        """检查性能指标"""
        if not result_dir:
            return 0.0, False, '未指定结果目录'
        
        metrics_file = Path(result_dir) / 'metrics.json'
        if not metrics_file.exists():
            return 0.0, False, 'metrics.json 不存在'
        
        with open(metrics_file) as f:
            metrics = json.load(f)
        
        metric_name = metric.get('metric_name', 'retention')
        threshold = metric['threshold']
        
        value = metrics.get(metric_name, 0)
        score = min(value / threshold, 1.0) if threshold > 0 else 0
        passed = value >= threshold
        
        return score, passed, f'{metric_name}={value:.2f} (要求：≥{threshold})'
    
    def _check_code_quality(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查代码质量"""
        path = self.workspace / metric['path']
        checks = metric.get('checks', [])
        threshold = metric['threshold']
        
        if not path.exists():
            return 0.0, False, '目录不存在'
        
        py_files = list(path.glob('*.py'))
        if not py_files:
            return 0.0, False, '无 Python 文件'
        
        # 执行质量检查
        quality_scores = []
        
        for f in py_files:
            content = f.read_text()
            file_scores = []
            
            if 'has_comments' in checks:
                has_comments = '#' in content
                file_scores.append(1.0 if has_comments else 0.0)
            
            if 'has_docstring' in checks:
                has_docstring = '"""' in content or "'''" in content
                file_scores.append(1.0 if has_docstring else 0.0)
            
            if 'modular' in checks:
                has_functions = 'def ' in content
                file_scores.append(1.0 if has_functions else 0.0)
            
            if file_scores:
                quality_scores.append(sum(file_scores) / len(file_scores))
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        score = avg_quality
        passed = avg_quality >= threshold
        
        return score, passed, f'质量评分 {avg_quality:.2f} (要求：≥{threshold})'
    
    def _check_reproducible(self, metric: Dict) -> Tuple[float, bool, str]:
        """检查结果可复现"""
        # 简化实现：检查是否有 metrics.json
        path = self.workspace / metric.get('path', 'results/')
        
        if not path.exists():
            return 0.0, False, '结果目录不存在'
        
        metrics_files = list(path.rglob('metrics.json'))
        if not metrics_files:
            return 0.0, False, '无 metrics.json 文件'
        
        # 如果有多个文件，检查一致性
        if len(metrics_files) > 1:
            # TODO: 实现一致性检查
            return 0.8, True, '多个结果文件 (未检查一致性)'
        
        return 1.0, True, '结果文件存在'
    
    def _generate_recommendations(self, failures: List[Dict]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        for failure in failures:
            metric = failure['metric']
            reason = failure['reason']
            
            if '文件' in reason or '无文件' in reason:
                recommendations.append(f'{metric}: 确保创建足够的输出文件')
            elif '字数' in reason or '字' in reason:
                recommendations.append(f'{metric}: 增加内容详细程度')
            elif '关键词' in reason:
                recommendations.append(f'{metric}: 确保包含必要的关键信息')
            elif '链接' in reason:
                recommendations.append(f'{metric}: 添加来源链接')
            elif '运行失败' in reason:
                recommendations.append(f'{metric}: 修复代码错误，确保可运行')
            elif '章节' in reason:
                recommendations.append(f'{metric}: 补充缺失的章节')
            else:
                recommendations.append(f'{metric}: {reason}')
        
        return recommendations
    
    def save_report(self, results: Dict, output_path: str):
        """保存验证报告"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 验证报告已保存：{output_file}")


# ============================================================
# 主程序
# ============================================================

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='验证 Agent 产出质量')
    parser.add_argument('agent_type', choices=['literature', 'research', 'code', 'analysis', 'writing'],
                       help='Agent 类型')
    parser.add_argument('--result-dir', '-r', help='结果目录')
    parser.add_argument('--output', '-o', help='输出报告路径')
    parser.add_argument('--workspace', '-w', default='/home/openclaw/.openclaw/workspace/obsidian-repo',
                       help='工作空间路径')
    
    args = parser.parse_args()
    
    verifier = Verifier(args.workspace)
    results = verifier.verify(args.agent_type, args.result_dir)
    
    if args.output:
        verifier.save_report(results, args.output)
    
    # 返回退出码
    sys.exit(0 if results['passed'] else 1)


if __name__ == '__main__':
    main()
