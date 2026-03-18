#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM/Agent 面试题目爬虫 - MVP 版本
数据源：牛客网、GitHub
"""

import os
import sys
import json
import hashlib
import traceback
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from sources.niuke import NiukeCrawler
from sources.github import GitHubCrawler
from processor import QuestionProcessor, AnswerGenerator
from notifier import notify_success, notify_error


class InterviewCrawler:
    def __init__(self, config=None):
        self.root_dir = Path(__file__).parent.parent.parent
        self.output_dir = self.root_dir / "obsidian-repo" / "40-Interview" / "LLM 面试题库"
        self.cache_dir = Path(__file__).parent / "cache"
        self.cache_dir.mkdir(exist_ok=True)
        
        # 关键词配置
        self.keywords = [
            "LLM 面试",
            "大模型 面试",
            "Agent 面试",
            "LLM 算法",
            "大语言模型 面经",
        ]
        
        # 加载缓存
        self.existing_questions = self.load_existing_questions()
    
    def load_existing_questions(self):
        """加载已有的题目（避免重复）"""
        cache_file = self.cache_dir / "questions_cache.json"
        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {q["id"]: q for q in data.get("questions", [])}
        return {}
    
    def save_cache(self, questions):
        """保存题目缓存"""
        cache_file = self.cache_dir / "questions_cache.json"
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "updated_at": datetime.now().isoformat(),
                "questions": list(questions.values())
            }, f, ensure_ascii=False, indent=2)
    
    def question_hash(self, question_text):
        """生成题目唯一 ID"""
        return hashlib.md5(question_text.strip().encode()).hexdigest()[:12]
    
    def crawl(self):
        """执行爬虫"""
        print(f"[{datetime.now()}] 开始抓取面试题目...")
        
        all_questions = []
        
        # 1. 牛客网
        print("[1/2] 抓取牛客网...")
        try:
            niuke = NiukeCrawler()
            niuke_questions = niuke.fetch(keywords=self.keywords)
            print(f"  ✓ 牛客网抓取 {len(niuke_questions)} 道题目")
            all_questions.extend(niuke_questions)
        except Exception as e:
            print(f"  ✗ 牛客网抓取失败：{e}")
        
        # 2. GitHub
        print("[2/2] 抓取 GitHub...")
        try:
            github = GitHubCrawler()
            github_questions = github.fetch()
            print(f"  ✓ GitHub 抓取 {len(github_questions)} 道题目")
            all_questions.extend(github_questions)
        except Exception as e:
            print(f"  ✗ GitHub 抓取失败：{e}")
        
        # 去重
        new_questions = []
        for q in all_questions:
            q_id = self.question_hash(q["text"])
            if q_id not in self.existing_questions:
                q["id"] = q_id
                new_questions.append(q)
        
        print(f"\n✓ 新增题目：{len(new_questions)} 道")
        
        # 更新缓存
        self.existing_questions.update({q["id"]: q for q in new_questions})
        self.save_cache(self.existing_questions)
        
        return new_questions
    
    def process_and_generate(self, questions):
        """处理题目并生成答案"""
        if not questions:
            print("没有新题目，跳过答案生成")
            return []
        
        print(f"\n开始生成答案...")
        processor = QuestionProcessor()
        generator = AnswerGenerator()
        
        processed = []
        for i, q in enumerate(questions, 1):
            print(f"  [{i}/{len(questions)}] 处理：{q['text'][:30]}...")
            
            # 分类
            category = processor.classify(q["text"])
            q["category"] = category
            
            # 生成答案
            answer = generator.generate(q["text"], category)
            q["answer"] = answer
            
            processed.append(q)
        
        return processed
    
    def save_to_markdown(self, questions):
        """保存为 Markdown 文件"""
        if not questions:
            return None
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 按日期保存
        filename = f"LLM 面试题库-{today}.md"
        filepath = self.output_dir / filename
        
        content = self.format_markdown(questions, today)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        print(f"\n✓ 已保存到：{filepath}")
        
        # 更新索引
        self.update_index(today, len(questions))
        
        # 发送通知
        try:
            categories = defaultdict(int)
            for q in questions:
                categories[q.get("category", "综合")] += 1
            
            notify_success(today, len(questions), dict(categories), str(filepath))
        except Exception as e:
            print(f"[通知] 发送失败：{e}")
        
        return filepath
    
    def format_markdown(self, questions, date):
        """格式化 Markdown 内容"""
        content = f"""# LLM/Agent 面试题库 - {date}

> 抓取时间：{date}
> 来源：牛客网、GitHub
> 本日新增：{len(questions)} 题

---

"""
        # 按分类分组
        from collections import defaultdict
        by_category = defaultdict(list)
        for q in questions:
            by_category[q["category"]].append(q)
        
        for category, qs in sorted(by_category.items()):
            content += f"## {category}\n\n"
            
            for i, q in enumerate(qs, 1):
                content += f"""### Q{i}: {q['text']}

**难度**: {q.get('difficulty', '⭐⭐⭐')}
**来源**: {q.get('source', '未知')}

#### 参考答案

{q.get('answer', '待生成...')}

---

"""
        
        content += f"""\n*最后更新：{date} | 小虾 🦐*
"""
        
        return content
    
    def update_index(self, date, count):
        """更新索引文件"""
        index_file = self.output_dir / "README.md"
        
        if index_file.exists():
            with open(index_file, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            content = """# LLM/Agent 面试题库

> 自动抓取 + 生成答案

---

## 📅 最新题目

"""
        
        # 添加到顶部
        new_line = f"- [{date}]({date}.md) - 新增 {count} 题\n"
        
        # 找到插入位置
        if "## 📅 最新题目" in content:
            lines = content.split("\n")
            insert_idx = lines.index("## 📅 最新题目") + 1
            lines.insert(insert_idx, new_line)
            content = "\n".join(lines)
        else:
            content += new_line
        
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(content)
    
    def run(self):
        """完整流程"""
        try:
            # 1. 抓取
            questions = self.crawl()
            
            # 2. 生成答案
            processed = self.process_and_generate(questions)
            
            # 3. 保存
            if processed:
                self.save_to_markdown(processed)
                return True
            
            return False
        
        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            tb = traceback.format_exc()
            print(f"\n❌ 运行失败：{error_msg}")
            
            try:
                notify_error(error_msg, tb)
            except:
                pass
            
            return False


if __name__ == "__main__":
    crawler = InterviewCrawler()
    success = crawler.run()
    sys.exit(0 if success else 1)
