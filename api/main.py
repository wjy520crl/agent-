from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent_framework.agents.research_agent import ResearchAgent
from agent_framework.agents.code_agent import CodeAgent
from agent_framework.agents.writing_agent import WritingAgent
from agent_framework.supervisor_agent import SupervisorAgent

app = FastAPI(title="多Agent架构系统 API", version="1.0.0")

# 挂载静态文件
if os.path.exists("api/static"):
    app.mount("/static", StaticFiles(directory="api/static"), name="static")

# 根路径返回前端页面
@app.get("/")
async def root():
    if os.path.exists("api/static/index.html"):
        return FileResponse("api/static/index.html")
    return {"message": "多Agent架构系统 API"}

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（开发环境）
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化Agent
research_agent = ResearchAgent()
code_agent = CodeAgent()
writing_agent = WritingAgent()
supervisor_agent = SupervisorAgent()

# 请求模型
class TaskRequest(BaseModel):
    agent_type: str
    task: str

class SmartRouteRequest(BaseModel):
    task: str
    use_smart_route: bool = True

# 响应模型
class TaskResponse(BaseModel):
    result: str
    agent_type: str

class SmartRouteResponse(BaseModel):
    task_type: str
    required_agents: List[str]
    reasoning: str
    result: Optional[str] = None

@app.post("/api/execute", response_model=TaskResponse)
async def execute_task(request: TaskRequest):
    """执行任务"""
    try:
        if request.agent_type == "research":
            result = research_agent.execute(request.task)
        elif request.agent_type == "code":
            result = code_agent.execute(request.task)
        elif request.agent_type == "writing":
            result = writing_agent.execute(request.task)
        elif request.agent_type == "multi":
            result = supervisor_agent.execute(request.task)
        else:
            raise HTTPException(status_code=400, detail="Invalid agent type")
        
        return TaskResponse(result=result, agent_type=request.agent_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/smart-route", response_model=SmartRouteResponse)
async def smart_route(request: SmartRouteRequest):
    """智能路由任务"""
    try:
        # 分析任务
        task_analysis = supervisor_agent.analyze_task(request.task)
        
        # 如果需要执行，根据分析结果执行
        result = None
        if request.use_smart_route:
            if len(task_analysis["required_agents"]) == 1:
                # 单个Agent，直接使用该Agent
                agent_name = task_analysis["required_agents"][0]
                if agent_name == "research":
                    result = research_agent.execute(request.task)
                elif agent_name == "code":
                    result = code_agent.execute(request.task)
                elif agent_name == "writing":
                    result = writing_agent.execute(request.task)
            else:
                # 多个Agent，使用SupervisorAgent
                result = supervisor_agent.execute(request.task)
        
        return SmartRouteResponse(
            task_type=task_analysis["task_type"],
            required_agents=task_analysis["required_agents"],
            reasoning=task_analysis.get("reasoning", "Task analyzed successfully"),
            result=result
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
