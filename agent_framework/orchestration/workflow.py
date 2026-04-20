from langgraph.graph import StateGraph, END
from typing import Dict, Any, Optional
from ..base_agent import Agent
from ..supervisor_agent import SupervisorAgent
from ..memory.shared_memory import SharedMemory

class WorkflowManager:
    def __init__(self):
        self.shared_memory = SharedMemory()
    
    def create_workflow(self, supervisor: SupervisorAgent) -> StateGraph:
        """创建工作流程"""
        # 定义状态类型
        class State:
            def __init__(self):
                self.task = ""
                self.context = {}
                self.results = {}
                self.current_agent = ""
        
        # 创建状态图
        workflow = StateGraph(State)
        
        # 定义节点
        def start_node(state: State) -> Dict[str, Any]:
            """开始节点"""
            return {"current_agent": "supervisor"}
        
        def supervisor_node(state: State) -> Dict[str, Any]:
            """监督者节点"""
            # 分析任务
            task_analysis = supervisor.analyze_task(state.task)
            
            # 分配子任务
            results = {}
            for agent_name in task_analysis["required_agents"]:
                if agent_name in supervisor.agents:
                    results[agent_name] = supervisor.assign_task(state.task, agent_name)
            
            # 汇总结果
            final_result = supervisor.synthesize_results(results)
            
            return {
                "results": results,
                "final_result": final_result
            }
        
        # 添加节点
        workflow.add_node("start", start_node)
        workflow.add_node("supervisor", supervisor_node)
        
        # 添加边
        workflow.set_entry_point("start")
        workflow.add_edge("start", "supervisor")
        workflow.add_edge("supervisor", END)
        
        return workflow
    
    def run_workflow(self, workflow: StateGraph, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """运行工作流程"""
        # 编译工作流程
        app = workflow.compile()
        
        # 运行工作流程
        result = app.invoke({
            "task": task,
            "context": context or {}
        })
        
        return result
