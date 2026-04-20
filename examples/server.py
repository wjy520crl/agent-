import http.server
import socketserver
import os

# 定义服务器端口
PORT = 8000

# 更改工作目录到examples文件夹
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 创建请求处理器
Handler = http.server.SimpleHTTPRequestHandler

# 启动服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"服务器运行在 http://localhost:{PORT}")
    print(f"测试表单地址: http://localhost:{PORT}/test_form.html")
    httpd.serve_forever()
