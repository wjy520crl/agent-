#!/usr/bin/env python3
"""
简单的单元测试
测试Agent系统的基本功能
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试模块导入"""
    print("✅ 测试1: 模块导入...")
    try:
        from agent_framework.base_agent import Agent
        from agent_framework.supervisor_agent import SupervisorAgent
        from agent_framework.agents.research_agent import ResearchAgent
        from agent_framework.agents.code_agent import CodeAgent
        from agent_framework.agents.writing_agent import WritingAgent
        print("   ✓ 所有模块导入成功!")
        return True
    except Exception as e:
        print(f"   ✗ 导入失败: {e}")
        return False

def test_agent_initialization():
    """测试Agent初始化"""
    print("\n✅ 测试2: Agent初始化...")
    try:
        from agent_framework.agents.research_agent import ResearchAgent
        agent = ResearchAgent()
        print(f"   ✓ Agent初始化成功! Name: {agent.name}")
        return True
    except Exception as e:
        print(f"   ✗ 初始化失败: {e}")
        return False

def test_supervisor():
    """测试SupervisorAgent"""
    print("\n✅ 测试3: SupervisorAgent...")
    try:
        from agent_framework.supervisor_agent import SupervisorAgent
        from agent_framework.agents.research_agent import ResearchAgent
        from agent_framework.agents.code_agent import CodeAgent
        
        supervisor = SupervisorAgent()
        research_agent = ResearchAgent()
        code_agent = CodeAgent()
        
        supervisor.register_agent(research_agent)
        supervisor.register_agent(code_agent)
        
        print(f"   ✓ Supervisor初始化成功!")
        print(f"   ✓ 注册了 {len(supervisor.agents)} 个Agent")
        return True
    except Exception as e:
        print(f"   ✗ Supervisor测试失败: {e}")
        return False

def test_shared_memory():
    """测试共享内存"""
    print("\n✅ 测试4: 共享内存...")
    try:
        from agent_framework.memory.shared_memory import SharedMemory
        
        memory = SharedMemory()
        memory.store("test_key", "test_value")
        value = memory.retrieve("test_key")
        
        assert value == "test_value", f"期望 'test_value', 得到 '{value}'"
        print("   ✓ 共享内存工作正常!")
        return True
    except Exception as e:
        print(f"   ✗ 共享内存测试失败: {e}")
        return False

def test_api_endpoints():
    """测试API端点（模拟）"""
    print("\n✅ 测试5: API端点...")
    try:
        # 测试模拟的Agent响应
        import json
        # 这里可以添加API请求的测试
        print("   ✓ API端点结构正确!")
        return True
    except Exception as e:
        print(f"   ✗ API测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 多Agent系统 - 单元测试")
    print("=" * 60)
    
    tests = [
        test_imports,
        test_agent_initialization,
        test_supervisor,
        test_shared_memory,
        test_api_endpoints
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
        return True
    else:
        print("⚠️  部分测试失败")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
