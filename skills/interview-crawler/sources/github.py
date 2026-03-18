#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub 面试题库爬虫
抓取开源面试仓库
"""

import requests
import re
from typing import List, Dict
from datetime import datetime


class GitHubCrawler:
    def __init__(self):
        self.repos = [
            "https://raw.githubusercontent.com/zhaochenggang/LLM-interview/main/README.md",
            "https://raw.githubusercontent.com/km1994/LLM_interview/main/README.md",
            "https://raw.githubusercontent.com/DjangoPeng/LLM-Quick-Course/main/README.md",
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }
    
    def fetch(self) -> List[Dict]:
        """从 GitHub 仓库抓取题目"""
        all_questions = []
        
        for repo_url in self.repos:
            try:
                questions = self.fetch_repo(repo_url)
                all_questions.extend(questions)
            except Exception as e:
                print(f"    仓库 {repo_url[:50]}... 抓取失败：{e}")
        
        return all_questions
    
    def fetch_repo(self, url: str) -> List[Dict]:
        """抓取单个仓库"""
        questions = []
        
        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            content = resp.text
            
            # 提取 Markdown 标题作为题目
            extracted = self.extract_questions(content)
            
            for q_text in extracted:
                questions.append({
                    "text": q_text,
                    "source": f"GitHub - {url.split('/')[3]}/{url.split('/')[4]}",
                    "url": url.replace("raw.githubusercontent.com", "github.com").replace("/main/", "/blob/main/"),
                    "crawl_time": datetime.now().isoformat(),
                })
        
        except Exception as e:
            pass
        
        return questions
    
    def extract_questions(self, content: str) -> List[str]:
        """从 Markdown 内容提取题目"""
        questions = []
        
        # 匹配 ### 或 ## 标题
        pattern = r'^#{2,3}\s+(.+)$'
        
        for line in content.split('\n'):
            match = re.match(pattern, line.strip())
            if match:
                title = match.group(1).strip()
                # 过滤：包含关键词且长度合适
                if self.is_valid_question(title):
                    questions.append(title)
        
        return questions[:20]  # 最多 20 题
    
    def is_valid_question(self, text: str) -> bool:
        """判断是否是有效的面试题目"""
        keywords = [
            "LLM", "Agent", "大模型", "Transformer", "Attention",
            "微调", "预训练", "RLHF", "Prompt", "LoRA", "PEFT",
            "RAG", "向量", "嵌入", "tokenizer", "显存", "推理",
        ]
        
        text_lower = text.lower()
        
        # 至少包含一个关键词
        has_keyword = any(kw.lower() in text_lower for kw in keywords)
        
        # 长度合适
        valid_length = 10 < len(text) < 150
        
        # 不是目录或链接
        not_nav = not any(x in text for x in ["目录", "TOC", "http", "www"])
        
        return has_keyword and valid_length and not_nav
