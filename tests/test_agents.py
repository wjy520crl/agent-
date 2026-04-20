import pytest
from agent_framework import Agent, SupervisorAgent, ResearchAgent, CodeAgent, DataAgent, WritingAgent

class TestAgent:
    def test_agent_initialization(self):
        """测试Agent初始化"""
        agent = ResearchAgent()
        assert agent.name == "research"
        assert agent.llm_model == "gpt-4"
    
    def test_supervisor_agent(self):
        """测试SupervisorAgent"""
        supervisor = SupervisorAgent()
        research_agent = ResearchAgent()
        supervisor.register_agent(research_agent)
        assert "research" in supervisor.agents
    
    def test_research_agent(self):
        """测试ResearchAgent"""
        research_agent = ResearchAgent()
        # 测试简单任务
        result = research_agent.execute("测试研究任务")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_code_agent(self):
        """测试CodeAgent"""
        code_agent = CodeAgent()
        # 测试简单代码生成
        result = code_agent.execute("打印'Hello, World!'")
        assert isinstance(result, str)
        assert "Hello, World!" in result
    
    def test_data_agent(self):
        """测试DataAgent"""
        data_agent = DataAgent()
        # 测试简单数据分析
        result = data_agent.execute("创建一个包含10个随机数的列表并计算平均值")
        assert isinstance(result, str)
    
    def test_writing_agent(self):
        """测试WritingAgent"""
        writing_agent = WritingAgent()
        # 测试简单写作任务
        result = writing_agent.execute("写一段关于人工智能的简短介绍")
        assert isinstance(result, str)
        assert len(result) > 0
