from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional
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
    allow_origins=["http://localhost:5175"],  # 前端域名
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

# 响应模型
class TaskResponse(BaseModel):
    result: str
    agent_type: str

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

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
