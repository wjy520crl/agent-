import time
import resource
import pytest
import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_framework import SupervisorAgent, ResearchAgent, CodeAgent, DataAgent, WritingAgent

class MultiDimensionTest:
    def __init__(self):
        # 初始化测试环境
        self.supervisor = SupervisorAgent()
        self.research_agent = ResearchAgent()
        self.code_agent = CodeAgent()
        self.data_agent = DataAgent()
        self.writing_agent = WritingAgent()
        
        # 注册Agent到Supervisor
        self.supervisor.register_agent(self.research_agent)
        self.supervisor.register_agent(self.code_agent)
        self.supervisor.register_agent(self.data_agent)
        self.supervisor.register_agent(self.writing_agent)
    
    def test_functionality(self):
        """测试各个Agent的功能"""
        print("=== 功能测试 ===")
        
        # 测试ResearchAgent
        print("测试 ResearchAgent...")
        research_task = "研究2026年人工智能的最新趋势"
        research_result = self.research_agent.execute(research_task)
        print(f"ResearchAgent 执行结果: {research_result[:100]}...")
        assert len(research_result) > 0
        
        # 测试CodeAgent
        print("\n测试 CodeAgent...")
        code_task = "创建一个Python函数，计算斐波那契数列的第10项"
        code_result = self.code_agent.execute(code_task)
        print(f"CodeAgent 执行结果: {code_result[:100]}...")
        assert len(code_result) > 0
        
        # 测试DataAgent
        print("\n测试 DataAgent...")
        data_task = "创建一个包含10个随机数的列表并计算平均值"
        data_result = self.data_agent.execute(data_task)
        print(f"DataAgent 执行结果: {data_result[:100]}...")
        assert len(data_result) > 0
        
        # 测试WritingAgent
        print("\n测试 WritingAgent...")
        writing_task = "写一段关于人工智能的简短介绍"
        writing_result = self.writing_agent.execute(writing_task)
        print(f"WritingAgent 执行结果: {writing_result[:100]}...")
        assert len(writing_result) > 0
        
        # 测试Multi-Agent协作
        print("\n测试 Multi-Agent 协作...")
        multi_task = "研究2026年人工智能的最新趋势，创建一个Python脚本可视化这些趋势，然后撰写一份详细的报告"
        multi_result = self.supervisor.execute(multi_task)
        print(f"Multi-Agent 协作结果: {multi_result[:100]}...")
        assert len(multi_result) > 0
        
        print("\n功能测试通过！")
    
    def test_performance(self):
        """测试系统性能"""
        print("\n=== 性能测试 ===")
        
        # 测试响应时间
        print("测试响应时间...")
        tasks = [
            ("研究任务", self.research_agent, "研究2026年人工智能的最新趋势"),
            ("代码任务", self.code_agent, "创建一个Python函数，计算斐波那契数列的第10项"),
            ("数据任务", self.data_agent, "创建一个包含10个随机数的列表并计算平均值"),
            ("写作任务", self.writing_agent, "写一段关于人工智能的简短介绍"),
            ("多Agent任务", self.supervisor, "研究2026年人工智能的最新趋势，创建一个Python脚本可视化这些趋势，然后撰写一份详细的报告")
        ]
        
        for task_name, agent, task in tasks:
            start_time = time.time()
            start_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            
            result = agent.execute(task)
            
            end_time = time.time()
            end_memory = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            
            execution_time = end_time - start_time
            memory_used = (end_memory - start_memory) / 1024  # 转换为MB
            
            print(f"{task_name}: 执行时间 = {execution_time:.2f}秒, 内存使用 = {memory_used:.2f}MB")
        
        print("\n性能测试完成！")
    
    def test_integration(self):
        """测试系统集成"""
        print("\n=== 集成测试 ===")
        
        # 测试任务分解和分配
        print("测试任务分解和分配...")
        complex_task = "研究2026年人工智能的最新趋势，创建一个Python脚本可视化这些趋势，然后撰写一份详细的报告"
        
        # 分析任务
        task_analysis = self.supervisor.analyze_task(complex_task)
        print(f"任务分析结果: {task_analysis}")
        assert "required_agents" in task_analysis
        
        # 执行任务
        result = self.supervisor.execute(complex_task)
        print(f"集成测试结果: {result[:100]}...")
        assert len(result) > 0
        
        print("\n集成测试通过！")
    
    def test_stability(self):
        """测试系统稳定性"""
        print("\n=== 稳定性测试 ===")
        
        # 连续执行多个任务
        print("测试连续执行多个任务...")
        tasks = [
            "研究2026年人工智能的最新趋势",
            "创建一个Python函数，计算斐波那契数列的第10项",
            "创建一个包含10个随机数的列表并计算平均值",
            "写一段关于人工智能的简短介绍",
            "研究2026年人工智能的最新趋势，创建一个Python脚本可视化这些趋势，然后撰写一份详细的报告"
        ]
        
        for i, task in enumerate(tasks):
            print(f"执行任务 {i+1}/{len(tasks)}...")
            result = self.supervisor.execute(task)
            assert len(result) > 0
            print(f"任务 {i+1} 执行成功")
        
        print("\n稳定性测试通过！")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始多维度测试...")
        
        try:
            self.test_functionality()
            self.test_performance()
            self.test_integration()
            self.test_stability()
            print("\n所有测试通过！")
        except Exception as e:
            print(f"\n测试失败: {str(e)}")

if __name__ == "__main__":
    test = MultiDimensionTest()
    test.run_all_tests()
