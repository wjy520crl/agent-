# 多Agent架构系统

一个基于多个专业智能体协作的系统，用于完成复杂任务，提升工作效率和质量。

## 项目结构

```
├── agent_framework/    # Agent框架核心代码
│   ├── agents/         # 专业Agent实现
│   │   ├── code_agent.py      # 代码生成和执行Agent
│   │   ├── data_agent.py      # 数据分析Agent
│   │   ├── research_agent.py  # 信息收集和分析Agent
│   │   └── writing_agent.py   # 内容创作Agent
│   ├── memory/         # 共享内存
│   ├── orchestration/  # 工作流编排
│   ├── tools/          # 工具集
│   ├── base_agent.py   # 基础Agent类
│   ├── config.py       # 配置文件
│   ├── llm_client.py   # LLM客户端
│   └── supervisor_agent.py  # 监督Agent
├── api/                # 后端API
│   └── main.py         # FastAPI应用
├── frontend/           # 前端Vue应用
├── examples/           # 示例代码
└── requirements.txt    # Python依赖
```

## 核心功能

- **多Agent协作**：多个专业Agent协同工作，完成复杂任务
- **研究功能**：收集和分析信息，提供研究报告
- **代码生成**：生成和执行代码，解决编程问题
- **内容创作**：撰写和编辑内容，提供高质量文本
- **Web界面**：直观的用户界面，方便用户交互

## 技术栈

- **后端**：Python, FastAPI
- **前端**：Vue 3, Vite
- **AI模型**：Claude 3

## 安装指南

### 后端安装

1. 克隆项目

```bash
git clone <repository-url>
cd multi-agent-system
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 配置API密钥

在 `agent_framework/config.py` 文件中配置您的API密钥：

```python
API_CONFIG = {
    "anthropic": {
        "api_key": "your-api-key",
        "api_url": "https://api.minimaxi.com/anthropic"
    }
}
```

4. 启动后端服务

```bash
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

### 前端安装

1. 进入前端目录

```bash
cd frontend
```

2. 安装依赖

```bash
npm install
```

3. 启动前端开发服务器

```bash
npm run dev
```

## 使用说明

1. 打开前端页面（默认 http://localhost:5173）
2. 选择Agent类型（Research、Code、Writing或Multi-Agent）
3. 输入任务描述
4. 点击"执行任务"按钮
5. 查看执行结果

## API文档

### 执行任务

- **Endpoint**: `/api/execute`
- **Method**: POST
- **Request Body**:

```json
{
  "agent_type": "research",
  "task": "研究人工智能在医疗领域的应用"
}
```

- **Response**:

```json
{
  "result": "# 研究结果...",
  "agent_type": "research"
}
```

### 健康检查

- **Endpoint**: `/api/health`
- **Method**: GET
- **Response**:

```json
{
  "status": "healthy"
}
```

## 示例

### 研究任务

```
任务：研究人工智能在医疗领域的应用
Agent类型：Research Agent
结果：详细的研究报告，包括AI在诊断辅助、药物研发和患者护理等方面的应用
```

### 代码任务

```
任务：生成一个Python函数，计算斐波那契数列的第n项
Agent类型：Code Agent
结果：生成的Python代码和执行结果
```

### 写作任务

```
任务：撰写一篇关于人工智能发展的文章
Agent类型：Writing Agent
结果：结构化的文章内容
```

### 多Agent协作

```
任务：分析人工智能对就业市场的影响
Agent类型：Multi-Agent
结果：综合多个Agent的分析结果，提供全面的报告
```

## 未来发展

- 扩展更多专业Agent
- 优化Agent之间的协作机制
- 增强系统的可扩展性和可维护性
- 添加更多工具和功能
- 改进用户界面和用户体验

## 贡献

欢迎贡献代码、报告问题或提出建议！

## 许可证

MIT License
