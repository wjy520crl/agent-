import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_framework import CodeAgent

# 初始化CodeAgent
code_agent = CodeAgent()

# 执行代码任务
task = "创建一个Python函数，计算斐波那契数列的第n项"
result = code_agent.execute(task)

# 打印结果
print("=== Code Agent Result ===")
print(result)
