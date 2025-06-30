from tavily import TavilyClient
from dotenv import load_dotenv
import os

load_dotenv()
tavily_api_key = os.getenv("TAVILY_API_KEY")

if not tavily_api_key:
    raise ValueError("TAVILY_API_KEY is not set")

def search_web(query: str, max_results: int = 10) -> str:
    """
    搜索网络信息
    Args:
        query: 搜索关键词
        max_results: 最大搜索结果数
    Returns:
        str: 搜索结果
    """
    tavily_client = TavilyClient(api_key=tavily_api_key)
    response = tavily_client.search(query, max_results=max_results)
    return response

if __name__ == "__main__":
    print(search_web("茅台的最新股价是多少？", max_results=2))