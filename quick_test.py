#!/usr/bin/env python3
"""
快速测试脚本 - 验证所有模块导入是否正常
"""

import sys
from pathlib import Path

def test_imports():
    """测试所有模块的导入"""
    print("🧪 开始导入测试...")
    
    try:
        # 测试基础模块导入
        print("📦 测试基础模块导入...")
        import config
        print("✅ config 模块导入成功")
        
        import utils
        print("✅ utils 模块导入成功")
        
        import api_client
        print("✅ api_client 模块导入成功")
        
        import nodes
        print("✅ nodes 模块导入成功")
        
        # 测试类的实例化
        print("\n🏗️ 测试类实例化...")
        
        from config import FluxKontextConfig
        config_instance = FluxKontextConfig()
        print("✅ FluxKontextConfig 实例化成功")
        
        from api_client import FluxKontextAPI, FluxKontextAPIError
        print("✅ FluxKontextAPI 和 FluxKontextAPIError 导入成功")
        
        from nodes import FluxKontextNode, FluxKontextAdvancedNode
        print("✅ ComfyUI 节点类导入成功")
        
        # 测试节点类型定义
        print("\n📋 测试节点类型定义...")
        basic_types = FluxKontextNode.INPUT_TYPES()
        advanced_types = FluxKontextAdvancedNode.INPUT_TYPES()
        print("✅ 节点输入类型定义正常")
        
        print("\n🎉 所有导入测试通过！")
        return True
        
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def test_api_key():
    """测试API密钥配置"""
    print("\n🔑 测试API密钥配置...")
    
    try:
        from config import FluxKontextConfig
        config = FluxKontextConfig()
        
        api_key = config.get_api_key()
        if api_key:
            print(f"✅ 找到API密钥: {api_key[:10]}...{api_key[-10:]}")
            return True
        else:
            print("⚠️ 未找到API密钥，请检查 .env 文件")
            return False
            
    except Exception as e:
        print(f"❌ API密钥测试失败: {e}")
        return False

def main():
    """主函数"""
    print("🚀 Flux-Kontext ComfyUI 节点快速测试")
    print("=" * 50)
    
    # 导入测试
    import_success = test_imports()
    
    # API密钥测试
    api_key_success = test_api_key()
    
    print("\n" + "=" * 50)
    print("📊 测试总结:")
    print(f"📦 模块导入: {'✅ 通过' if import_success else '❌ 失败'}")
    print(f"🔑 API密钥: {'✅ 配置' if api_key_success else '⚠️ 未配置'}")
    
    if import_success:
        print("\n🎉 项目已准备就绪！")
        if api_key_success:
            print("💡 可以运行 'python test_api.py' 进行完整测试")
        else:
            print("💡 请在 .env 文件中配置API密钥后运行完整测试")
    else:
        print("\n❌ 项目配置有问题，请检查导入错误")
    
    return 0 if import_success else 1

if __name__ == "__main__":
    sys.exit(main()) 