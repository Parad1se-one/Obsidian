#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书通知模块
"""

import json
import requests
from typing import Optional
from datetime import datetime


class FeishuNotifier:
    """飞书消息通知"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url
    
    def send_interview_summary(self, date: str, question_count: int, categories: dict, filepath: str):
        """发送面试题库抓取摘要"""
        
        # 分类统计
        category_stats = "\n".join([f"  • {k}: {v}题" for k, v in sorted(categories.items(), key=lambda x: -x[1])])
        
        content = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": f"📚 LLM 面试题库 - {date}",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": f"✅ 今日抓取完成\n\n"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"📊 新增题目：{question_count} 道\n"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"📁 分类统计：\n{category_stats}\n\n"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"📄 文件位置：\n{filepath}\n\n"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"⏰ 下次运行：明天 09:00"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        
        return self._send(content)
    
    def send_error_notification(self, error_msg: str, traceback: str = ""):
        """发送错误通知"""
        
        content = {
            "msg_type": "post",
            "content": {
                "post": {
                    "zh_cn": {
                        "title": "❌ 面试爬虫运行失败",
                        "content": [
                            [
                                {
                                    "tag": "text",
                                    "text": f"⚠️ 错误信息：\n{error_msg}\n\n"
                                }
                            ],
                            [
                                {
                                    "tag": "text",
                                    "text": f"🔍 详情：\n{traceback[:500] if traceback else '无'}"
                                }
                            ]
                        ]
                    }
                }
            }
        }
        
        return self._send(content)
    
    def _send(self, content: dict) -> bool:
        """发送消息"""
        if not self.webhook_url:
            print("[通知] Webhook URL 未配置，跳过通知")
            return False
        
        try:
            resp = requests.post(self.webhook_url, json=content, timeout=10)
            resp.raise_for_status()
            
            result = resp.json()
            if result.get("code") == 0 or result.get("StatusCode") == 0:
                print("[通知] 消息发送成功")
                return True
            else:
                print(f"[通知] 发送失败：{result}")
                return False
        
        except Exception as e:
            print(f"[通知] 发送异常：{e}")
            return False


def notify_success(date: str, question_count: int, categories: dict, filepath: str):
    """快捷发送成功通知"""
    notifier = FeishuNotifier()
    return notifier.send_interview_summary(date, question_count, categories, filepath)


def notify_error(error_msg: str, traceback: str = ""):
    """快捷发送错误通知"""
    notifier = FeishuNotifier()
    return notifier.send_error_notification(error_msg, traceback)
