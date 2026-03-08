#!/usr/bin/env python3
"""
search_tool.py - Python 搜索工具 (基于 Whoogle)
用法:
    from search_tool import search, search_urls, search_first
    
    # 搜索并返回结果列表
    results = search("python tutorial", count=10)
    
    # 只返回 URL 列表
    urls = search_urls("github", count=5)
    
    # 返回第一条结果
    first = search_first("weather beijing")
"""

import requests
import re
from html import unescape
from typing import List, Dict, Optional

WHOOGL_URL = "http://127.0.0.1:5000"
DEFAULT_TIMEOUT = 30


class SearchError(Exception):
    """搜索异常"""
    pass


def check_whoogle(url: str = WHOOGL_URL) -> bool:
    """检查 Whoogle 是否可用"""
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except Exception:
        return False


def search(query: str, count: int = 10, timeout: int = DEFAULT_TIMEOUT) -> List[Dict[str, str]]:
    """
    搜索并返回结果列表
    
    Args:
        query: 搜索关键词
        count: 返回结果数量 (默认 10)
        timeout: 请求超时时间 (默认 30 秒)
    
    Returns:
        搜索结果列表，每项包含 {'title': str, 'url': str}
    
    Raises:
        SearchError: 搜索失败时抛出
    """
    if not query:
        raise SearchError("搜索关键词不能为空")
    
    if not check_whoogle():
        raise SearchError(f"Whoogle 不可用 (地址：{WHOOGL_URL})")
    
    try:
        response = requests.get(
            f"{WHOOGL_URL}/search",
            params={"q": query},
            timeout=timeout
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise SearchError(f"搜索请求失败：{e}")
    
    html = response.text
    
    # 解析搜索结果 (Whoogle 格式)
    results = []
    title_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)'
    seen = set()
    
    for match in re.finditer(title_pattern, html):
        url = unescape(match.group(1).replace('&amp;', '&'))
        title = unescape(re.sub(r'<[^>]+>', '', match.group(2)))
        
        # 过滤无效结果
        if not url.startswith('http') or 'google.com/maps' in url:
            continue
        if url in seen:
            continue
        
        seen.add(url)
        results.append({'title': title, 'url': url})
        
        if len(results) >= count:
            break
    
    return results


def search_urls(query: str, count: int = 5, timeout: int = DEFAULT_TIMEOUT) -> List[str]:
    """
    搜索并返回 URL 列表
    
    Args:
        query: 搜索关键词
        count: 返回 URL 数量 (默认 5)
        timeout: 请求超时时间
    
    Returns:
        URL 列表
    """
    results = search(query, count=count, timeout=timeout)
    return [r['url'] for r in results]


def search_first(query: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[str]:
    """
    搜索并返回第一条结果的 URL
    
    Args:
        query: 搜索关键词
        timeout: 请求超时时间
    
    Returns:
        第一条结果的 URL，无结果返回 None
    """
    urls = search_urls(query, count=1, timeout=timeout)
    return urls[0] if urls else None


def search_with_snippet(query: str, count: int = 10, timeout: int = DEFAULT_TIMEOUT) -> List[Dict[str, str]]:
    """
    搜索并返回包含摘要的结果
    
    Args:
        query: 搜索关键词
        count: 返回结果数量
        timeout: 请求超时时间
    
    Returns:
        搜索结果列表，每项包含 {'title': str, 'url': str, 'snippet': str}
    """
    if not query:
        raise SearchError("搜索关键词不能为空")
    
    if not check_whoogle():
        raise SearchError(f"Whoogle 不可用 (地址：{WHOOGL_URL})")
    
    try:
        response = requests.get(
            f"{WHOOGL_URL}/search",
            params={"q": query},
            timeout=timeout
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise SearchError(f"搜索请求失败：{e}")
    
    html = response.text
    
    # 提取标题和 URL
    results = []
    title_pattern = r'<div class="result__body"[^>]*>.*?class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+).*?class="result__snippet"[^>]*>([^<]+)'
    
    for match in re.finditer(title_pattern, html, re.DOTALL):
        url = unescape(match.group(1))
        title = unescape(match.group(2))
        snippet = unescape(re.sub(r'<[^>]+>', '', match.group(3)))
        results.append({
            'title': title,
            'url': url,
            'snippet': snippet
        })
        
        if len(results) >= count:
            break
    
    # 如果没有提取到摘要，尝试简单模式
    if not results:
        title_pattern = r'class="result__a"[^>]*href="([^"]+)"[^>]*>([^<]+)'
        for match in re.finditer(title_pattern, html):
            url = unescape(match.group(1))
            title = unescape(match.group(2))
            results.append({
                'title': title,
                'url': url,
                'snippet': ''
            })
            
            if len(results) >= count:
                break
    
    return results


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python search_tool.py \"关键词\" [数量]")
        print("示例：python search_tool.py \"python tutorial\" 10")
        sys.exit(1)
    
    query = sys.argv[1]
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    try:
        results = search(query, count=count)
        
        print("=" * 60)
        print(f"搜索结果：{query}")
        print("=" * 60)
        
        for i, r in enumerate(results, 1):
            print(f"\n{i}. {r['title']}")
            print(f"   {r['url']}")
        
    except SearchError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
