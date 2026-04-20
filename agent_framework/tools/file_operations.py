import os
from typing import Optional

class FileOperationsTool:
    def __init__(self):
        pass
    
    def read(self, file_path: str) -> str:
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def write(self, file_path: str, content: str, mode: str = 'w') -> str:
        """写入文件内容"""
        try:
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            with open(file_path, mode, encoding='utf-8') as f:
                f.write(content)
            return f"File written successfully: {file_path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"
    
    def list_files(self, directory: str) -> str:
        """列出目录中的文件"""
        try:
            files = os.listdir(directory)
            return "\n".join(files) if files else "No files found"
        except Exception as e:
            return f"Error listing files: {str(e)}"
    
    def exists(self, file_path: str) -> bool:
        """检查文件是否存在"""
        return os.path.exists(file_path)
