import logging
import os
import requests
from bs4 import BeautifulSoup 
from config import Config
from duckduckgo_search import DDGS

# 配置日志（指定UTF-8编码）
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename='logs/search.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)
logger = logging.getLogger(__name__)

class Search:
    @staticmethod
    def search(keywords):
        """执行网络搜索并返回内容"""
        try:
            with DDGS() as ddgs:
                results = ddgs.text(
                    keywords=keywords,
                    max_results=Config.SEARCH_MAX_RESULTS,
                    timelimit='y'
                )
                return [{
                    "title": r.get("title", "无标题"),
                    "url": r.get("href", "#"),
                    "content": r.get("body", "无内容")
                } for r in results]
        except Exception as e:
            logger.error(f"搜索失败: {str(e)}")
            return []

if __name__ == "__main__":
    class TestConfig:
        SEARCH_MAX_RESULTS = 3  # 测试时设为3条结果
    
    Config = TestConfig
    test_keywords = ["量子计算原理"]
    
    for keyword in test_keywords:
        print(f"\n===== 测试关键词: '{keyword}' =====")
        results = Search.search(keyword)
        
        if results:
            print(f"成功获取 {len(results)} 条结果:")
            for i, result in enumerate(results, 1):
                print(f"\n结果 {i}:")
                print(f"  标题: {result['title']}")
                print(f"  URL: {result['url']}")
                print(f"  内容: {result['content'][:500]}...")  # 显示前100个字符
        else:
            print("警告：未获取到搜索结果，可能原因：")
            print("- 关键词是否正确？尝试改为通用词（如“量子计算”）")
            print("- 是否被网络限制？尝试访问DuckDuckGo确认")
            print("- API是否有调用频率限制？")
        
        