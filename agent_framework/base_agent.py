from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class Agent(ABC):
    def __init__(self, name: str, llm_model: str = "gpt-4"):
        self.name = name
        self.llm_model = llm_model
        self.state = {}
    
    @abstractmethod
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行任务并返回结果"""
        pass
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """使用工具执行操作"""
        # 子类需要实现具体的工具调用逻辑
        raise NotImplementedError("Subclasses must implement use_tool method")
    
    def get_state(self) -> Dict[str, Any]:
        """获取Agent状态"""
        return self.state
    
    def set_state(self, state: Dict[str, Any]):
        """设置Agent状态"""
        self.state.update(state)
