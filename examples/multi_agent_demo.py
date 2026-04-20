import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_framework import SupervisorAgent, ResearchAgent, CodeAgent, WritingAgent

# 初始化SupervisorAgent
supervisor = SupervisorAgent()

# 注册专业Agent
research_agent = ResearchAgent()
code_agent = CodeAgent()
writing_agent = WritingAgent()

supervisor.register_agent(research_agent)
supervisor.register_agent(code_agent)
supervisor.register_agent(writing_agent)

# 执行复杂任务
task = "研究2026年人工智能的最新趋势，创建一个Python脚本可视化这些趋势，然后撰写一份详细的报告"
result = supervisor.execute(task)

# 打印结果
print("=== Multi-Agent Collaboration Result ===")
print(result)
