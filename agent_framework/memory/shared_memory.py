from typing import Dict, Any, Optional

class SharedMemory:
    def __init__(self):
        self.memory = {}
    
    def store(self, key: str, value: Any):
        """存储信息到共享内存"""
        self.memory[key] = value
    
    def retrieve(self, key: str) -> Optional[Any]:
        """从共享内存检索信息"""
        return self.memory.get(key)
    
    def clear(self):
        """清空共享内存"""
        self.memory.clear()
    
    def get_all(self) -> Dict[str, Any]:
        """获取所有内存内容"""
        return self.memory
    
    def update(self, data: Dict[str, Any]):
        """批量更新内存内容"""
        self.memory.update(data)
