from typing import Dict, Any, List, Optional
from .base_agent import Agent
from .memory.shared_memory import SharedMemory
from .llm_client import LLMClient

class SupervisorAgent(Agent):
    def __init__(self, llm_model: str = "claude-3-opus-20240229"):
        super().__init__("supervisor", llm_model)
        self.agents = {}
        self.shared_memory = SharedMemory()
        self.llm_client = LLMClient()
    
    def register_agent(self, agent: Agent):
        """注册专业Agent"""
        self.agents[agent.name] = agent
    
    def analyze_task(self, task: str) -> Dict[str, Any]:
        """分析任务并确定需要的Agent"""
        # 使用LLM分析任务类型和所需专业知识
        prompt = f"""
        Analyze the following task and determine:
        1. What type of task is this? (research, code, data analysis, writing, etc.)
        2. Which specialized agents are needed to complete this task?
        3. How should the task be decomposed into sub-tasks?
        
        Task: {task}
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a task analyzer for a multi-agent system."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return {
            "task_type": "complex",
            "required_agents": list(self.agents.keys()),
            "sub_tasks": [task]
        }
    
    def assign_task(self, sub_task: str, agent_name: str) -> str:
        """将子任务分配给指定Agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not registered")
        
        agent = self.agents[agent_name]
        context = self.shared_memory.get_all()
        result = agent.execute(sub_task, context)
        
        # 将结果存储到共享内存
        self.shared_memory.store(f"{agent_name}_result", result)
        
        return result
    
    def synthesize_results(self, results: Dict[str, str]) -> str:
        """汇总所有Agent的结果"""
        # 使用LLM综合结果
        prompt = f"""
        Synthesize the following results from different agents into a comprehensive response:
        
        {results}
        
        Provide a well-structured, cohesive summary that addresses the original task.
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a result synthesizer for a multi-agent system."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        return response
    
    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> str:
        """执行复杂任务"""
        # 分析任务
        task_analysis = self.analyze_task(task)
        
        # 分配子任务给相应的Agent
        results = {}
        for agent_name in task_analysis["required_agents"]:
            if agent_name in self.agents:
                results[agent_name] = self.assign_task(task, agent_name)
        
        # 汇总结果
        final_result = self.synthesize_results(results)
        
        return final_result
