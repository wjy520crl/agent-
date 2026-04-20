import subprocess
import tempfile
import os

class CodeExecutorTool:
    def __init__(self):
        pass
    
    def execute(self, code: str, language: str = "python") -> str:
        """执行代码"""
        if language.lower() == "python":
            return self.execute_python(code)
        else:
            return f"Language {language} not supported"
    
    def execute_python(self, code: str) -> str:
        """执行Python代码"""
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
        except subprocess.TimeoutExpired:
            # 清理临时文件
            if 'temp_file' in locals():
                os.unlink(temp_file)
            return "Error: Execution timed out"
        except Exception as e:
            # 清理临时文件
            if 'temp_file' in locals():
                os.unlink(temp_file)
            return f"Execution error: {str(e)}"
