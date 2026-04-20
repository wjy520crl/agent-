import requests
import json
from .config import API_CONFIG, MODEL_CONFIG

class LLMClient:
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        self.config = API_CONFIG.get(provider)
        if not self.config:
            raise ValueError(f"Provider {provider} not configured")
    
    def generate(self, messages: list, model: str = None, **kwargs) -> str:
        """生成文本"""
        if self.provider == "anthropic":
            return self._anthropic_generate(messages, model, **kwargs)
        else:
            raise ValueError(f"Provider {self.provider} not supported")
    
    def _anthropic_generate(self, messages: list, model: str = None, **kwargs) -> str:
        """使用Anthropic API生成文本"""
        model = model or MODEL_CONFIG["default_model"]
        
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.config["api_key"]
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", 1024),
            "temperature": kwargs.get("temperature", 0.7)
        }
        
        try:
            response = requests.post(
                self.config["api_url"] + "/v1/messages",
                headers=headers,
                data=json.dumps(data)
            )
            response.raise_for_status()
            
            result = response.json()
            # 检查响应结构
            if "content" in result and len(result["content"]) > 0:
                # 遍历content数组，找到text类型的内容
                for item in result["content"]:
                    if "type" in item and item["type"] == "text":
                        if "text" in item:
                            return item["text"]
                # 如果没有找到text类型的内容，返回第一个元素
                content = result["content"][0]
                if "text" in content:
                    return content["text"]
                elif "message" in content:
                    return content["message"]
                else:
                    return f"Error: Unexpected content structure: {content}"
            else:
                return f"Error: No content in response"
        except Exception as e:
            print(f"Error details: {str(e)}")
            return f"Error calling Anthropic API: {str(e)}"
