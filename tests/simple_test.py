import time
import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agent_framework import ResearchAgent, CodeAgent, WritingAgent

class SimpleTest:
    def __init__(self):
        # 初始化测试环境
        self.research_agent = ResearchAgent()
        self.code_agent = CodeAgent()
        self.writing_agent = WritingAgent()
    
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
        
        # 测试WritingAgent
        print("\n测试 WritingAgent...")
        writing_task = "写一段关于人工智能的简短介绍"
        writing_result = self.writing_agent.execute(writing_task)
        print(f"WritingAgent 执行结果: {writing_result[:100]}...")
        assert len(writing_result) > 0
        
        print("\n功能测试通过！")
    
    def test_performance(self):
        """测试系统性能"""
        print("\n=== 性能测试 ===")
        
        # 测试响应时间
        print("测试响应时间...")
        tasks = [
            ("研究任务", self.research_agent, "研究2026年人工智能的最新趋势"),
            ("代码任务", self.code_agent, "创建一个Python函数，计算斐波那契数列的第10项"),
            ("写作任务", self.writing_agent, "写一段关于人工智能的简短介绍")
        ]
        
        for task_name, agent, task in tasks:
            start_time = time.time()
            result = agent.execute(task)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"{task_name}: 执行时间 = {execution_time:.2f}秒")
        
        print("\n性能测试完成！")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始多维度测试...")
        
        try:
            self.test_functionality()
            self.test_performance()
            print("\n所有测试通过！")
        except Exception as e:
            print(f"\n测试失败: {str(e)}")

if __name__ == "__main__":
    test = SimpleTest()
    test.run_all_tests()
