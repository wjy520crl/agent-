#!/usr/bin/env python3
"""
多Agent系统 API 服务器
提供 REST API 接口供前端调用
"""
import json
import sys
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
import time

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 模拟Agent响应（避免真实API调用）
class MockAgentSystem:
    """模拟Agent系统，用于测试"""
    
    @staticmethod
    def execute_research_task(task):
        """模拟研究任务"""
        return f"""# 研究结果报告

根据您的任务要求，我进行了全面的信息收集和深度分析，发现了以下关键洞察：

## 核心发现

### 1. 信息点一
这一发现揭示了问题的本质，提供了重要的视角。通过多源数据交叉验证，我们确认了这一结论的可靠性。

### 2. 信息点二
这一维度的分析补充了前者的不足，形成了完整的认知图景。数据显示这一趋势正在加速发展。

### 3. 信息点三
这是最具突破性的发现，重新定义了我们对问题的理解。建议将此作为战略决策的核心依据。

## 结论
这些信息相互印证，共同构成了完整的认知框架。基于这些发现，我们可以做出更加明智的决策。"""
    
    @staticmethod
    def execute_code_task(task):
        """模拟代码任务"""
        return f"""# 代码生成与执行报告

```python
def fibonacci(n):
    \"\"\"计算斐波那契数列的第n项\"\"\"
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

# 测试代码
for i in range(1, 11):
    print(f"F({{i}}) = {{fibonacci(i)}}")
```

## 执行结果
```
F(1) = 1
F(2) = 1
F(3) = 2
F(4) = 3
F(5) = 5
F(6) = 8
F(7) = 13
F(8) = 21
F(9) = 34
F(10) = 55
```

## 分析
代码已成功生成并执行，运行结果正确。斐波那契数列展现了指数增长的特性。"""
    
    @staticmethod
    def execute_writing_task(task):
        """模拟写作任务"""
        return f"""# 人工智能：未来的引擎

## 引言

人工智能（Artificial Intelligence）正以前所未有的速度重塑我们的世界。从1956年达特茅斯会议的萌芽，到今天深度学习的突破，AI已经走过了漫长而曲折的道路。

## 核心技术架构

### 机器学习
让计算机从数据中自动学习和改进，而无需明确编程。这是AI革命的核心驱动力。

### 深度学习
模拟人脑神经网络的层次结构，在图像识别、自然语言处理等领域取得了突破性进展。

### 自然语言处理
使计算机能够理解、解释和生成人类语言，实现人机之间的自然沟通。

### 计算机视觉
赋予计算机"看"的能力，从图像和视频中提取有意义的信息。

## 未来展望
随着技术的不断成熟，人工智能将在医疗健康、金融、教育、制造等领域发挥越来越重要的作用，成为推动社会进步的核心动力。"""
    
    @staticmethod
    def execute_multi_task(task):
        """模拟多Agent协作任务"""
        return f"""# 多智能体协作综合报告

## Research Agent 贡献
进行了全面的文献调研和数据收集，识别了关键趋势和机会点。发现了三个核心洞察，为后续工作奠定了基础。

## Code Agent 贡献
基于研究结果，开发了核心算法和实现代码。代码经过充分测试，性能指标优秀。

## Writing Agent 贡献
整合所有发现，撰写了这份综合报告。确保了内容的逻辑性、准确性和可读性。

## 综合结论

### 关键发现
1. **发现一**：通过多智能体协作，我们获得了比单一智能更全面的洞察
2. **发现二**：分布式处理显著提升了任务完成的效率和质量
3. **发现三**：不同专业智能体的互补创造了新的可能性

### 行动建议
1. 建立常态化的多智能体协作机制
2. 持续优化智能体之间的沟通协议
3. 扩展智能体类型，覆盖更多专业领域"""

class AgentAPIHandler(BaseHTTPRequestHandler):
    """处理API请求的handler"""
    
    def _set_headers(self, status_code=200):
        """设置响应头"""
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self._set_headers()
    
    def do_GET(self):
        """处理GET请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/status':
            # 返回系统状态
            status = {
                'status': 'ok',
                'agents': ['research', 'code', 'data', 'writing'],
                'system': 'running'
            }
            self._set_headers()
            self.wfile.write(json.dumps(status).encode('utf-8'))
        elif parsed_path.path == '/api/agents':
            # 返回Agent列表
            agents = [
                {
                    'id': 'research',
                    'name': 'Research Agent',
                    'description': '信息收集与深度分析专家'
                },
                {
                    'id': 'code',
                    'name': 'Code Agent',
                    'description': '代码生成与执行专家'
                },
                {
                    'id': 'data',
                    'name': 'Data Agent',
                    'description': '数据分析与可视化专家'
                },
                {
                    'id': 'writing',
                    'name': 'Writing Agent',
                    'description': '内容创作与文案专家'
                }
            ]
            self._set_headers()
            self.wfile.write(json.dumps(agents).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
    
    def do_POST(self):
        """处理POST请求"""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/execute':
            # 处理任务执行请求
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            agent_type = data.get('agentType', 'research')
            task = data.get('task', '')
            
            print(f"收到任务 - Agent: {agent_type}, Task: {task[:50]}...")
            
            # 模拟处理延迟
            time.sleep(2)
            
            # 根据agent类型返回不同结果
            result = ''
            if agent_type == 'research':
                result = MockAgentSystem.execute_research_task(task)
            elif agent_type == 'code':
                result = MockAgentSystem.execute_code_task(task)
            elif agent_type == 'writing':
                result = MockAgentSystem.execute_writing_task(task)
            elif agent_type == 'multi':
                result = MockAgentSystem.execute_multi_task(task)
            
            response = {
                'success': True,
                'agentType': agent_type,
                'result': result,
                'timestamp': time.time()
            }
            
            self._set_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode('utf-8'))
    
    def log_message(self, format, *args):
        """自定义日志输出"""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_api_server(host='localhost', port=8001):
    """启动API服务器"""
    server_address = (host, port)
    httpd = HTTPServer(server_address, AgentAPIHandler)
    print(f"\n🚀 Agent API服务器启动成功!")
    print(f"📍 地址: http://{host}:{port}")
    print(f"📡 API端点:")
    print(f"   - GET  /api/status    - 获取系统状态")
    print(f"   - GET  /api/agents    - 获取Agent列表")
    print(f"   - POST /api/execute   - 执行Agent任务")
    print(f"\n按 Ctrl+C 停止服务器\n")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 服务器正在停止...")
        httpd.shutdown()
        print("✅ 服务器已停止")

if __name__ == '__main__':
    run_api_server()
