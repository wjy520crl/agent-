import requests
from bs4 import BeautifulSoup

class WebSearchTool:
    def __init__(self):
        pass
    
    def search(self, query: str, num_results: int = 5) -> str:
        """执行Web搜索"""
        # 这里使用DuckDuckGo的API进行搜索
        # 实际应用中可能需要使用更强大的搜索API
        url = f"https://duckduckgo.com/html/?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            # 提取搜索结果
            for result in soup.select('.result')[:num_results]:
                title_element = result.select_one('.result__a')
                url_element = result.select_one('.result__url')
                snippet_element = result.select_one('.result__snippet')
                
                if title_element and url_element:
                    title = title_element.text
                    url = url_element.text
                    snippet = snippet_element.text if snippet_element else ""
                    results.append(f"- {title} ({url})\n  {snippet}")
            
            return "\n".join(results) if results else "No results found"
        except Exception as e:
            return f"Error searching: {str(e)}"
