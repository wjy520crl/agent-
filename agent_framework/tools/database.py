import sqlite3
from typing import Dict, Any

class DatabaseTool:
    def __init__(self):
        pass
    
    def query(self, db_path: str, query: str) -> str:
        """执行数据库查询"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute(query)
            
            # 获取列名
            columns = [description[0] for description in cursor.description]
            
            # 获取结果
            rows = cursor.fetchall()
            
            conn.close()
            
            # 格式化结果
            if rows:
                result = " | ".join(columns) + "\n"
                result += "-" * (len(" | ".join(columns))) + "\n"
                for row in rows:
                    result += " | ".join(str(item) for item in row) + "\n"
                return result
            else:
                return "No results found"
        except Exception as e:
            return f"Error querying database: {str(e)}"
    
    def execute(self, db_path: str, query: str) -> str:
        """执行数据库操作（插入、更新、删除等）"""
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute(query)
            conn.commit()
            
            affected_rows = cursor.rowcount
            conn.close()
            
            return f"Operation successful. Affected rows: {affected_rows}"
        except Exception as e:
            return f"Error executing operation: {str(e)}"
