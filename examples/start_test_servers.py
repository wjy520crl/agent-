#!/usr/bin/env python3
"""
启动测试服务器
同时启动前端静态文件服务器和后端API服务器
"""
import sys
import os
import subprocess
import time
import threading
import webbrowser

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def start_api_server():
    """启动API服务器"""
    print("🚀 正在启动 API 服务器...")
    api_script = os.path.join(os.path.dirname(__file__), 'api_server.py')
    return subprocess.Popen([sys.executable, api_script])

def start_static_server():
    """启动静态文件服务器"""
    print("🌐 正在启动前端服务器...")
    static_script = os.path.join(os.path.dirname(__file__), 'server.py')
    return subprocess.Popen([sys.executable, static_script])

def wait_for_server(host, port, timeout=10):
    """等待服务器启动"""
    import socket
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def main():
    print("=" * 60)
    print("🦌 DeerFlow - 多Agent系统测试服务器")
    print("=" * 60)
    
    # 启动服务器
    api_process = start_api_server()
    time.sleep(1)  # 给API服务器一点时间先启动
    static_process = start_static_server()
    
    try:
        # 等待服务器启动
        print("\n⏳ 正在等待服务器启动...")
        api_ready = wait_for_server('localhost', 8001)
        static_ready = wait_for_server('localhost', 8000)
        
        if api_ready and static_ready:
            print("\n✅ 所有服务器启动成功!")
            print("\n" + "=" * 60)
            print("📡 服务地址:")
            print("   - 前端页面: http://localhost:8000/agent_dashboard.html")
            print("   - API服务:  http://localhost:8001")
            print("\n" + "=" * 60)
            
            # 自动打开浏览器
            print("\n🌐 正在打开浏览器...")
            time.sleep(1)
            webbrowser.open('http://localhost:8000/agent_dashboard.html')
            
            print("\n📝 按 Ctrl+C 停止所有服务器")
            print("=" * 60 + "\n")
            
            # 保持运行
            while True:
                time.sleep(1)
        else:
            print("❌ 服务器启动失败")
            api_process.terminate()
            static_process.terminate()
            
    except KeyboardInterrupt:
        print("\n\n👋 正在停止服务器...")
        api_process.terminate()
        static_process.terminate()
        print("✅ 所有服务器已停止")
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        api_process.terminate()
        static_process.terminate()

if __name__ == '__main__':
    main()
