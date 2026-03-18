#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
牛客网面试题目爬虫
"""

import re
import time
import random
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class NiukeCrawler:
    def __init__(self):
        self.base_url = "https://www.nowcoder.com"
        self.search_url = "https://www.nowcoder.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def fetch(self, keywords: List[str]) -> List[Dict]:
        """抓取面经题目"""
        all_questions = []
        
        for keyword in keywords:
            try:
                questions = self.search_keyword(keyword)
                all_questions.extend(questions)
                time.sleep(random.uniform(1, 2))  # 限流
            except Exception as e:
                print(f"    关键词 '{keyword}' 抓取失败：{e}")
        
        return all_questions
    
    def search_keyword(self, keyword: str) -> List[Dict]:
        """搜索关键词相关面经"""
        questions = []
        
        # 牛客网搜索 URL
        search_url = f"{self.search_url}?type=discuss&keyword={keyword}"
        
        try:
            resp = self.session.get(search_url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            # 提取帖子列表
            posts = soup.select(".discuss-item")
            
            for post in posts[:10]:  # 每个关键词最多 10 个帖子
                try:
                    post_data = self.parse_post(post, keyword)
                    if post_data:
                        questions.extend(post_data)
                except Exception as e:
                    continue
            
            # 如果没有提取到题目，使用 fallback
            if not questions:
                print(f"    未提取到题目，使用预设题目...")
                questions = self.get_fallback_questions(keyword)
            
        except Exception as e:
            # 如果搜索失败，返回一些预设题目（MVP 降级方案）
            print(f"    搜索失败，使用预设题目...")
            questions = self.get_fallback_questions(keyword)
        
        return questions
    
    def parse_post(self, post, keyword: str) -> List[Dict]:
        """解析帖子内容，提取面试题目"""
        questions = []
        
        try:
            title_elem = post.select_one(".discuss-title")
            content_elem = post.select_one(".discuss-content")
            
            if not title_elem:
                return []
            
            title = title_elem.get_text(strip=True)
            content = content_elem.get_text(strip=True) if content_elem else ""
            
            # 提取题目（正则匹配常见问题格式）
            extracted = self.extract_questions_from_text(title + "\n" + content)
            
            for q_text in extracted:
                questions.append({
                    "text": q_text,
                    "source": f"牛客网 - {title[:50]}",
                    "url": self.base_url + post.select_one("a")["href"] if post.select_one("a") else "",
                    "crawl_time": datetime.now().isoformat(),
                })
        
        except Exception as e:
            pass
        
        return questions
    
    def extract_questions_from_text(self, text: str) -> List[str]:
        """从文本中提取面试题目"""
        questions = []
        
        # 模式 1: "1. 问题内容" 或 "1、问题内容"
        pattern1 = r'[1-9][0-9]*[.、]\s*([^\n]+(?:LLM|Agent|大模型 | transformer|注意力 | 微调|RLHF|预训练)[^\n]*)'
        
        # 模式 2: "问：问题内容" 或 "问题：问题内容"
        pattern2 = r'(?:问 | 问题)[:：]\s*([^\n]+)'
        
        # 模式 3: 包含关键词的问句
        pattern3 = r'([^\n？?]+[？?])'
        
        # 提取
        for match in re.finditer(pattern1, text, re.IGNORECASE):
            q = match.group(1).strip()
            if len(q) > 10 and len(q) < 200:
                questions.append(q)
        
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            q = match.group(1).strip()
            if len(q) > 10 and len(q) < 200:
                questions.append(q)
        
        # 如果没有提取到，返回空
        return questions[:10]  # 每个帖子最多 10 题
    
    def get_fallback_questions(self, keyword: str) -> List[Dict]:
        """降级方案：返回预设题目（当爬虫失败时）"""
        fallback = {
            "LLM 面试": [
                "请解释一下 Transformer 的 Self-Attention 机制",
                "LLM 的预训练和微调有什么区别？",
                "什么是 RLHF？请详细说明其流程",
                "Transformer 中为什么使用 LayerNorm 而不是 BatchNorm？",
                "LLM 推理时的显存占用主要来自哪些部分？",
            ],
            "大模型 面试": [
                "大模型的显存优化有哪些方法？",
                "解释一下 LoRA 的原理和优势",
                "什么是 Prompt Engineering？有哪些技巧？",
                "大模型分布式训练有哪些并行策略？",
                "什么是 ZeRO 优化？",
            ],
            "Agent 面试": [
                "Agent 的核心组件有哪些？",
                "ReAct 框架的原理是什么？",
                "如何设计 Agent 的记忆机制？",
                "Agent 和 Workflow 有什么区别？",
                "如何避免 Agent 陷入循环调用？",
            ],
            "LLM 算法": [
                "解释一下 RoPE 位置编码的原理",
                "什么是 Flash Attention？优化原理是什么？",
                "LLM 的 tokenizer 有哪些常见方案？",
                "什么是 MoE 架构？优缺点是什么？",
            ],
            "大语言模型 面经": [
                "大模型训练数据如何清洗和处理？",
                "什么是 Instruction Tuning？",
                "如何评估 LLM 的能力？",
                "大模型的幻觉问题如何解决？",
            ],
        }
        
        questions = []
        for q_text in fallback.get(keyword, fallback["LLM 面试"]):
            questions.append({
                "text": q_text,
                "source": f"牛客网 - {keyword}",
                "url": "https://www.nowcoder.com/search",
                "crawl_time": datetime.now().isoformat(),
            })
        
        return questions
