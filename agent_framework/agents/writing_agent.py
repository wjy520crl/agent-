from typing import Dict, Any, Optional
from ..base_agent import Agent
from ..llm_client import LLMClient

class WritingAgent(Agent):
    def __init__(self, llm_model: str = "claude-3-opus-20240229"):
        super().__init__("writing", llm_model)
        self.llm_client = LLMClient()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行写作任务"""
        prompt = f"""
        You are a writing agent. Create content for the following task:
        
        {task}
        
        Provide well-structured, engaging, and professional content that meets the requirements.
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a professional writing agent with expertise in creating high-quality content."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """使用写作相关工具"""
        if tool_name == "summarize":
            text = kwargs.get("text", "")
            return self.summarize(text)
        elif tool_name == "translate":
            text = kwargs.get("text", "")
            target_language = kwargs.get("target_language", "English")
            return self.translate(text, target_language)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
    
    def summarize(self, text: str) -> str:
        """总结文本"""
        prompt = f"""
        Summarize the following text in a concise and clear manner:
        
        {text}
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are an expert summarizer."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def translate(self, text: str, target_language: str) -> str:
        """翻译文本"""
        prompt = f"""
        Translate the following text to {target_language}:
        
        {text}
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": f"You are an expert translator. Translate the text to {target_language}."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
