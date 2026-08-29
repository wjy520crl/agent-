from typing import Dict, Any, Optional
from ..base_agent import Agent
from ..llm_client import LLMClient
import pandas as pd
import matplotlib.pyplot as plt
import tempfile
import os

class DataAgent(Agent):
    def __init__(self, llm_model: str = "claude-3-opus-20240229"):
        super().__init__("data", llm_model)
        self.llm_client = LLMClient()
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行数据任务"""
        # 生成数据分析代码
        code = self.generate_data_analysis_code(task)
        
        # 执行代码
        result = self.execute_code(code)
        
        # 生成结果解释
        explanation = self.generate_explanation(task, code, result)
        
        return f"Data Analysis Code:\n```python\n{code}\n```\n\nAnalysis Result:\n{result}\n\nResult Explanation:\n{explanation}"
    
    def generate_explanation(self, task: str, code: str, result: str) -> str:
        """生成结果解释"""
        prompt = f"""
        You are a data agent. Provide a clear and comprehensive explanation of the following data analysis results:
        
        Task: {task}
        
        Code:
        {code}
        
        Result:
        {result}
        
        Explain what the analysis is doing, what the results mean, and any insights or recommendations based on the results.
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a professional data analyst擅长解释数据分析结果并提供有洞察力的见解。"},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def generate_data_analysis_code(self, task: str) -> str:
        """生成数据分析代码"""
        prompt = f"""
        You are a data agent. Generate Python code to perform the following data analysis task:
        
        {task}
        
        Provide only the code, no explanations. Make sure the code is correct and complete. Include necessary imports.
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a professional data agent with expertise in data analysis using pandas and matplotlib."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def execute_code(self, code: str) -> str:
        """执行数据代码"""
        try:
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # 执行代码
            import subprocess
            result = subprocess.run(
                ['python3', temp_file],
                capture_output=True,
                text=True,
                timeout=60
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
        """使用数据相关工具"""
        if tool_name == "pandas":
            # 这里可以实现pandas相关操作
            return "Pandas tool used (simulated)"
        elif tool_name == "matplotlib":
            # 这里可以实现matplotlib相关操作
            return "Matplotlib tool used (simulated)"
        else:
            raise ValueError(f"Unknown tool: {tool_name}")
