# 🧪 前后端测试指南

## 📋 概述

本文档说明如何对多Agent系统进行前后端测试。

## 🚀 快速开始

### 方式一：一键启动（推荐）

```bash
cd /workspace
python examples/start_test_servers.py
```

这将同时启动：
- 🌐 前端服务器 (http://localhost:8000)
- 🔧 API服务器 (http://localhost:8001)

浏览器会自动打开测试页面！

### 方式二：手动启动

#### 1. 启动后端API服务器

```bash
cd /workspace/examples
python api_server.py
```

API服务器运行在 `http://localhost:8001`

#### 2. 启动前端服务器

在另一个终端窗口中：

```bash
cd /workspace/examples
python server.py
```

前端服务器运行在 `http://localhost:8000`

#### 3. 打开浏览器

访问：`http://localhost:8000/agent_dashboard.html`

## 🧪 测试内容

### 1. 单元测试

```bash
cd /workspace
python tests/basic_test.py
```

测试项目：
- ✅ 项目文件结构
- ✅ 前端文件完整性
- ✅ API服务器代码语法
- ✅ 前端HTML结构
- ✅ 后端模块文件
- ✅ 启动脚本语法

### 2. 功能测试

在浏览器中打开测试页面后，测试以下功能：

#### 🔹 Agent选择测试
- [ ] 选择不同的Agent类型（Research/Code/Writing/Multi）
- [ ] 验证下拉菜单正常工作

#### 🔹 任务提交测试
- [ ] 输入测试任务描述
- [ ] 点击"执行任务"按钮
- [ ] 验证加载动画显示
- [ ] 验证结果正确显示

#### 🔹 结果展示测试
- [ ] 验证标题渲染（H1/H2/H3）
- [ ] 验证代码块展示
- [ ] 验证时间戳更新

#### 🔹 系统状态显示
- [ ] 验证状态指示器显示
- [ ] 验证Agent列表展示

### 3. API端点测试

使用curl或Postman测试API：

#### 获取系统状态
```bash
curl http://localhost:8001/api/status
```

预期响应：
```json
{
  "status": "ok",
  "agents": ["research", "code", "data", "writing"],
  "system": "running"
}
```

#### 获取Agent列表
```bash
curl http://localhost:8001/api/agents
```

#### 执行任务
```bash
curl -X POST http://localhost:8001/api/execute \
  -H "Content-Type: application/json" \
  -d '{"agentType":"research","task":"测试任务"}'
```

## 📁 文件结构

```
/workspace/
├── agent_framework/          # 后端核心模块
│   ├── base_agent.py         # Agent基类
│   ├── supervisor_agent.py   # 监督者Agent
│   ├── agents/               # 专业Agent
│   ├── memory/               # 共享内存
│   └── config.py             # 配置文件
├── examples/                 # 示例和前端
│   ├── agent_dashboard.html  # 前端界面（新版）
│   ├── api_server.py         # 后端API服务器
│   ├── server.py             # 静态文件服务器
│   └── start_test_servers.py # 一键启动脚本
└── tests/                    # 测试文件
    └── basic_test.py         # 基础测试
```

## 🎨 前端特点

### 设计风格
- 简约米色/棕色主题（DeerFlow风格）
- 清晰的视觉层次
- 平滑的动画过渡
- 响应式布局

### 主要组件
- 侧边栏导航
- Agent卡片网格
- 任务配置表单
- 系统状态显示
- 结果展示区域

## 🔧 故障排除

### 端口被占用
如果8000或8001端口被占用，可以修改对应脚本中的端口号。

### API连接失败
前端会自动降级到模拟模式，不影响功能测试。

### 页面无法打开
确认两个服务器都在正常运行，并检查防火墙设置。

## 📊 测试检查清单

### 后端测试
- [ ] 服务器成功启动
- [ ] API端点响应正常
- [ ] JSON格式正确
- [ ] CORS设置正确

### 前端测试
- [ ] 页面正常加载
- [ ] 样式正确应用
- [ ] 交互功能正常
- [ ] 响应式布局工作

### 集成测试
- [ ] 前后端通信正常
- [ ] 数据正确传输
- [ ] 错误处理完善
- [ ] 性能可接受

## 🎯 下一步

测试完成后，可以：
1. 集成真实的LLM API
2. 添加更多Agent类型
3. 实现更复杂的工作流
4. 添加用户认证功能
5. 优化性能和用户体验
