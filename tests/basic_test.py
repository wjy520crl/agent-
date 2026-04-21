#!/usr/bin/env python3
"""
基础测试 - 不依赖外部库
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_file_structure():
    """测试项目文件结构"""
    print("✅ 测试1: 项目文件结构...")
    try:
        # 检查核心文件是否存在
        assert os.path.exists('agent_framework'), "agent_framework目录不存在"
        assert os.path.exists('examples'), "examples目录不存在"
        assert os.path.exists('tests'), "tests目录不存在"
        assert os.path.exists('agent_framework/base_agent.py'), "base_agent.py不存在"
        assert os.path.exists('agent_framework/supervisor_agent.py'), "supervisor_agent.py不存在"
        print("   ✓ 项目结构正确!")
        return True
    except Exception as e:
        print(f"   ✗ 文件结构测试失败: {e}")
        return False

def test_frontend_files():
    """测试前端文件"""
    print("\n✅ 测试2: 前端文件...")
    try:
        assert os.path.exists('examples/agent_dashboard.html'), "agent_dashboard.html不存在"
        assert os.path.exists('examples/server.py'), "server.py不存在"
        assert os.path.exists('examples/api_server.py'), "api_server.py不存在"
        assert os.path.exists('examples/start_test_servers.py'), "start_test_servers.py不存在"
        print("   ✓ 前端文件齐全!")
        return True
    except Exception as e:
        print(f"   ✗ 前端文件测试失败: {e}")
        return False

def test_api_server_code():
    """测试API服务器代码"""
    print("\n✅ 测试3: API服务器代码...")
    try:
        import ast
        with open('examples/api_server.py', 'r', encoding='utf-8') as f:
            code = f.read()
        # 尝试解析Python代码
        ast.parse(code)
        print("   ✓ API服务器代码语法正确!")
        return True
    except Exception as e:
        print(f"   ✗ API服务器代码测试失败: {e}")
        return False

def test_frontend_html():
    """测试前端HTML"""
    print("\n✅ 测试4: 前端HTML...")
    try:
        with open('examples/agent_dashboard.html', 'r', encoding='utf-8') as f:
            content = f.read()
        # 检查关键元素
        assert '<!DOCTYPE html>' in content, "缺少DOCTYPE"
        assert '<html' in content, "缺少HTML标签"
        assert 'DeerFlow' in content, "应该包含DeerFlow品牌"
        assert 'taskForm' in content, "应该包含任务表单"
        print("   ✓ 前端HTML结构正确!")
        return True
    except Exception as e:
        print(f"   ✗ 前端HTML测试失败: {e}")
        return False

def test_backend_modules():
    """测试后端模块（不实际导入）"""
    print("\n✅ 测试5: 后端模块...")
    try:
        # 检查文件是否存在且有内容
        modules_to_check = [
            'agent_framework/base_agent.py',
            'agent_framework/supervisor_agent.py',
            'agent_framework/memory/shared_memory.py',
            'agent_framework/config.py',
        ]
        for module in modules_to_check:
            assert os.path.exists(module), f"{module} 不存在"
            with open(module, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content.strip()) > 0, f"{module} 是空的"
        print("   ✓ 后端模块文件齐全!")
        return True
    except Exception as e:
        print(f"   ✗ 后端模块测试失败: {e}")
        return False

def test_startup_scripts():
    """测试启动脚本"""
    print("\n✅ 测试6: 启动脚本...")
    try:
        import ast
        with open('examples/start_test_servers.py', 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print("   ✓ 启动脚本语法正确!")
        return True
    except Exception as e:
        print(f"   ✗ 启动脚本测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 多Agent系统 - 基础测试")
    print("=" * 60)
    
    tests = [
        test_file_structure,
        test_frontend_files,
        test_api_server_code,
        test_frontend_html,
        test_backend_modules,
        test_startup_scripts
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"   ✗ 测试异常: {e}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"📊 测试结果: {passed}/{total} 通过")
    print("=" * 60)
    
    if passed == total:
        print("🎉 所有测试通过!")
        print("\n📝 下一步: 运行 'python examples/start_test_servers.py' 启动测试服务器")
        return True
    else:
        print("⚠️  部分测试失败")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
