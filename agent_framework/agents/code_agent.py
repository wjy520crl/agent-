from typing import Dict, Any, Optional
from ..base_agent import Agent
from ..llm_client import LLMClient
import subprocess
import tempfile
import os

class CodeAgent(Agent):
    def __init__(self, llm_model: str = "claude-3-opus-20240229"):
        super().__init__("code", llm_model)
        self.llm_client = LLMClient()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行代码任务"""
        # 生成代码
        code = self.generate_code(task)
        
        # 执行代码
        result = self.execute_code(code)
        
        return f"Generated Code:\n```python\n{code}\n```\n\nExecution Result:\n{result}"
    
    def generate_code(self, task: str) -> str:
        """生成代码"""
        prompt = f"""
        You are a code agent. Generate Python code to solve the following task:
        
        {task}
        
        Provide only the code, no explanations. Make sure the code is correct and complete.
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a professional code agent with expertise in Python programming."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def execute_code(self, code: str) -> str:
        """执行代码"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # 执行代码
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 清理临时文件
            os.unlink(temp_file)
            
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"Execution error: {str(e)}"
    
    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """使用代码相关工具"""
        if tool_name == "code_executor":
            code = kwargs.get("code", "")
            return self.execute_code(code)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
