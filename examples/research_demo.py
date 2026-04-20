import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_framework import ResearchAgent

# 初始化ResearchAgent
research_agent = ResearchAgent()

# 执行研究任务
task = "研究2026年人工智能的最新趋势和发展方向"
result = research_agent.execute(task)

# 打印结果
print("=== Research Agent Result ===")
print(result)
