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
        
        # 自动注册所有专业Agent
        from .agents.research_agent import ResearchAgent
        from .agents.code_agent import CodeAgent
        from .agents.writing_agent import WritingAgent
        
        self.register_agent(ResearchAgent())
        self.register_agent(CodeAgent())
        self.register_agent(WritingAgent())
    
    def register_agent(self, agent: Agent):
        """注册专业Agent"""
        self.agents[agent.name] = agent
    
    def analyze_task(self, task: str) -> Dict[str, Any]:
        """分析任务并确定需要的Agent"""
        # 使用LLM分析任务类型和所需专业知识
        prompt = f"""
        Analyze the following task and provide a JSON response with the following structure:
        {{
            "task_type": "one of: research, code, writing, complex",
            "required_agents": ["list of agent names needed: research, code, writing"],
            "sub_tasks": ["list of sub-tasks if needed"],
            "reasoning": "brief explanation of why these agents were chosen"
        }}
        
        Task classification guide:
        - "research": needs information gathering, fact checking, or topic investigation
        - "code": needs programming, code generation, or code analysis
        - "writing": needs content creation, editing, or text generation
        - "complex": needs multiple types of expertise
        
        Task: {task}
        """
        
        response = self.llm_client.generate(
            messages=[
                {"role": "system", "content": "You are a task analyzer for a multi-agent system. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            model=self.llm_model
        )
        
        try:
            # 尝试解析JSON响应
            import json
            result = json.loads(response)
            
            # 确保required_agents是有效的Agent列表
            valid_agents = set(self.agents.keys())
            result["required_agents"] = [agent for agent in result.get("required_agents", []) if agent in valid_agents]
            
            # 如果没有找到任何Agent，默认使用所有
            if not result["required_agents"]:
                result["required_agents"] = list(self.agents.keys())
                result["task_type"] = "complex"
            
            return result
        except Exception as e:
            # 如果解析失败，使用启发式方法
            task_lower = task.lower()
            required_agents = []
            
            if any(keyword in task_lower for keyword in ["code", "program", "function", "algorithm", "python", "javascript", "bug", "debug"]):
                required_agents.append("code")
            
            if any(keyword in task_lower for keyword in ["research", "search", "find", "investigate", "study", "analyze", "information"]):
                required_agents.append("research")
            
            if any(keyword in task_lower for keyword in ["write", "content", "article", "essay", "document", "text", "summary", "translate"]):
                required_agents.append("writing")
            
            if not required_agents:
                required_agents = list(self.agents.keys())
                task_type = "complex"
            elif len(required_agents) == 1:
                task_type = required_agents[0]
            else:
                task_type = "complex"
            
            return {
                "task_type": task_type,
                "required_agents": required_agents,
                "sub_tasks": [task],
                "reasoning": "Task analyzed heuristically"
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
