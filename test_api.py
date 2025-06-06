#!/usr/bin/env python3
"""
Flux-Kontext API 完整测试脚本
测试所有API功能，包括文生图、图生图、参数测试等
"""

import os
import sys
import json
import time
import traceback
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加当前目录到Python路径，以便导入我们的模块
sys.path.insert(0, str(Path(__file__).parent))

from config import FluxKontextConfig
from api_client import FluxKontextAPI, FluxKontextAPIError
from utils import download_image, validate_url, parse_image_urls

class FluxKontextTester:
    """Flux-Kontext API测试器"""
    
    def __init__(self):
        """初始化测试器"""
        self.config = FluxKontextConfig()
        self.api_client = None
        self.test_results = []
        self.output_dir = Path("test_outputs")
        self.output_dir.mkdir(exist_ok=True)
        
        # 测试用的示例图片URL
        self.test_image_urls = [
            "https://tuziai.oss-cn-shenzhen.aliyuncs.com/style/default_style_small.png",
            "https://tuziai.oss-cn-shenzhen.aliyuncs.com/small/4-old.png"
        ]
    
    def log(self, message: str, level: str = "INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")
        
        if level == "ERROR":
            print("-" * 50)
            traceback.print_exc()
            print("-" * 50)
    
    def save_test_result(self, test_name: str, success: bool, details: Dict[str, Any]):
        """保存测试结果"""
        result = {
            "test_name": test_name,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        self.test_results.append(result)
    
    def test_api_key_validation(self) -> bool:
        """测试1: API密钥验证"""
        self.log("🔑 测试API密钥验证...")
        
        try:
            api_key = self.config.get_api_key()
            if not api_key:
                self.log("❌ 未找到API密钥", "ERROR")
                self.save_test_result("API密钥验证", False, {"error": "未找到API密钥"})
                return False
            
            self.log(f"✅ 找到API密钥: {api_key[:10]}...{api_key[-10:]}")
            
            # 创建API客户端
            self.api_client = FluxKontextAPI(config=self.config)
            
            # 测试API状态
            status = self.api_client.get_api_status()
            self.log(f"📊 API状态: {json.dumps(status, ensure_ascii=False, indent=2)}")
            
            self.save_test_result("API密钥验证", True, {"api_key_found": True, "status": status})
            return True
            
        except Exception as e:
            self.log(f"❌ API密钥验证失败: {str(e)}", "ERROR")
            self.save_test_result("API密钥验证", False, {"error": str(e)})
            return False
    
    def test_basic_text_to_image(self) -> bool:
        """测试2: 基础文生图功能"""
        self.log("🎨 测试基础文生图功能...")
        
        if not self.api_client:
            self.log("❌ API客户端未初始化", "ERROR")
            return False
        
        try:
            prompt = "一只可爱的橘猫坐在阳光下，高质量，4K"
            
            self.log(f"📝 提示词: {prompt}")
            
            # 调用API
            response = self.api_client.generate_image(
                prompt=prompt,
                aspect_ratio="1:1",
                output_format="png",
                safety_tolerance=2
            )
            
            self.log(f"📥 API响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            # 检查响应格式
            if "data" not in response or not response["data"]:
                self.log("❌ API响应格式错误", "ERROR")
                self.save_test_result("基础文生图", False, {"error": "响应格式错误", "response": response})
                return False
            
            image_url = response["data"][0]["url"]
            self.log(f"🖼️ 图片URL: {image_url}")
            
            # 下载图片
            image_path = self.output_dir / "test_text_to_image.png"
            if self.download_and_save_image(image_url, image_path):
                self.log(f"✅ 图片已保存到: {image_path}")
                self.save_test_result("基础文生图", True, {
                    "prompt": prompt,
                    "image_url": image_url,
                    "image_path": str(image_path),
                    "response": response
                })
                return True
            else:
                self.log("❌ 图片下载失败", "ERROR")
                self.save_test_result("基础文生图", False, {"error": "图片下载失败"})
                return False
                
        except FluxKontextAPIError as e:
            self.log(f"❌ API错误: {str(e)}", "ERROR")
            self.save_test_result("基础文生图", False, {"error": f"API错误: {str(e)}"})
            return False
        except Exception as e:
            self.log(f"❌ 未知错误: {str(e)}", "ERROR")
            self.save_test_result("基础文生图", False, {"error": f"未知错误: {str(e)}"})
            return False
    
    def test_image_to_image(self) -> bool:
        """测试3: 图生图功能"""
        self.log("🖼️ 测试图生图功能...")
        
        if not self.api_client:
            self.log("❌ API客户端未初始化", "ERROR")
            return False
        
        try:
            # 使用参考图片URL
            reference_url = self.test_image_urls[0]
            prompt = f"{reference_url} 让这个女人带上墨镜，衣服换成红色"
            
            self.log(f"📝 提示词: {prompt}")
            
            # 调用API
            response = self.api_client.generate_image(
                prompt=prompt,
                aspect_ratio="16:9",
                output_format="jpeg",
                safety_tolerance=3
            )
            
            self.log(f"📥 API响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            if "data" not in response or not response["data"]:
                self.log("❌ API响应格式错误", "ERROR")
                self.save_test_result("图生图", False, {"error": "响应格式错误"})
                return False
            
            image_url = response["data"][0]["url"]
            self.log(f"🖼️ 生成图片URL: {image_url}")
            
            # 下载图片
            image_path = self.output_dir / "test_image_to_image.jpg"
            if self.download_and_save_image(image_url, image_path):
                self.log(f"✅ 图片已保存到: {image_path}")
                self.save_test_result("图生图", True, {
                    "prompt": prompt,
                    "reference_url": reference_url,
                    "image_url": image_url,
                    "image_path": str(image_path),
                    "response": response
                })
                return True
            else:
                self.log("❌ 图片下载失败", "ERROR")
                self.save_test_result("图生图", False, {"error": "图片下载失败"})
                return False
                
        except Exception as e:
            self.log(f"❌ 图生图测试失败: {str(e)}", "ERROR")
            self.save_test_result("图生图", False, {"error": str(e)})
            return False
    
    def test_multi_image_reference(self) -> bool:
        """测试4: 多图参考功能"""
        self.log("🖼️🖼️ 测试多图参考功能...")
        
        if not self.api_client:
            self.log("❌ API客户端未初始化", "ERROR")
            return False
        
        try:
            # 使用多个参考图片
            url1 = self.test_image_urls[0]
            url2 = self.test_image_urls[1]
            prompt = f"{url1} {url2} 请将P2中的人物替换为P1中的人物风格"
            
            self.log(f"📝 多图提示词: {prompt}")
            
            # 解析URL
            urls, clean_prompt = parse_image_urls(prompt)
            self.log(f"🔍 解析到的URL: {urls}")
            self.log(f"🔍 清理后的提示词: {clean_prompt}")
            
            # 调用API
            response = self.api_client.generate_image(
                prompt=prompt,
                aspect_ratio="4:3",
                output_format="png",
                safety_tolerance=4
            )
            
            self.log(f"📥 API响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
            
            if "data" not in response or not response["data"]:
                self.log("❌ API响应格式错误", "ERROR")
                self.save_test_result("多图参考", False, {"error": "响应格式错误"})
                return False
            
            image_url = response["data"][0]["url"]
            self.log(f"🖼️ 生成图片URL: {image_url}")
            
            # 下载图片
            image_path = self.output_dir / "test_multi_image_reference.png"
            if self.download_and_save_image(image_url, image_path):
                self.log(f"✅ 图片已保存到: {image_path}")
                self.save_test_result("多图参考", True, {
                    "prompt": prompt,
                    "reference_urls": urls,
                    "clean_prompt": clean_prompt,
                    "image_url": image_url,
                    "image_path": str(image_path),
                    "response": response
                })
                return True
            else:
                self.log("❌ 图片下载失败", "ERROR")
                self.save_test_result("多图参考", False, {"error": "图片下载失败"})
                return False
                
        except Exception as e:
            self.log(f"❌ 多图参考测试失败: {str(e)}", "ERROR")
            self.save_test_result("多图参考", False, {"error": str(e)})
            return False
    
    def test_all_parameters(self) -> bool:
        """测试5: 全参数测试"""
        self.log("⚙️ 测试所有参数...")
        
        if not self.api_client:
            self.log("❌ API客户端未初始化", "ERROR")
            return False
        
        test_cases = [
            {
                "name": "种子测试",
                "params": {
                    "prompt": "一朵美丽的玫瑰花",
                    "seed": 12345,
                    "aspect_ratio": "9:16",
                    "output_format": "png",
                    "safety_tolerance": 1,
                    "prompt_upsampling": True
                }
            },
            {
                "name": "宽高比测试",
                "params": {
                    "prompt": "壮观的山脉风景",
                    "aspect_ratio": "21:9",
                    "output_format": "jpeg",
                    "safety_tolerance": 5
                }
            },
            {
                "name": "安全容忍度测试",
                "params": {
                    "prompt": "创意艺术作品",
                    "aspect_ratio": "3:4",
                    "output_format": "png",
                    "safety_tolerance": 6,
                    "prompt_upsampling": False
                }
            }
        ]
        
        all_success = True
        
        for i, test_case in enumerate(test_cases):
            try:
                self.log(f"🧪 执行测试: {test_case['name']}")
                self.log(f"📋 参数: {json.dumps(test_case['params'], ensure_ascii=False, indent=2)}")
                
                # 调用API
                response = self.api_client.generate_image(**test_case['params'])
                
                self.log(f"📥 API响应: {json.dumps(response, ensure_ascii=False, indent=2)}")
                
                if "data" not in response or not response["data"]:
                    self.log(f"❌ {test_case['name']} 响应格式错误", "ERROR")
                    all_success = False
                    continue
                
                image_url = response["data"][0]["url"]
                self.log(f"🖼️ 图片URL: {image_url}")
                
                # 下载图片
                filename = f"test_params_{i+1}_{test_case['name'].replace(' ', '_')}.{test_case['params']['output_format']}"
                image_path = self.output_dir / filename
                
                if self.download_and_save_image(image_url, image_path):
                    self.log(f"✅ {test_case['name']} 成功，图片保存到: {image_path}")
                else:
                    self.log(f"❌ {test_case['name']} 图片下载失败", "ERROR")
                    all_success = False
                
                # 短暂延迟，避免请求过快
                time.sleep(2)
                
            except Exception as e:
                self.log(f"❌ {test_case['name']} 失败: {str(e)}", "ERROR")
                all_success = False
        
        self.save_test_result("全参数测试", all_success, {"test_cases": test_cases})
        return all_success
    
    def test_chat_api(self) -> bool:
        """测试6: Chat格式API"""
        self.log("💬 测试Chat格式API...")
        
        if not self.api_client:
            self.log("❌ API客户端未初始化", "ERROR")
            self.save_test_result("Chat API", False, {"error": "API客户端未初始化"})
            return False
        
        try:
            messages = [
                {
                    "role": "user",
                    "content": "A golden retriever running on the grass on a sunny day"
                }
            ]
            
            self.log(f"💬 Chat消息: {json.dumps(messages, ensure_ascii=False, indent=2)}")
            
            # 调用Chat API，期望返回一个图片URL
            image_url = self.api_client.generate_image_chat(messages)
            
            self.log(f"🖼️ Chat API返回的图片URL: {image_url}")
            
            # 验证返回的是否是有效的URL
            if not validate_url(image_url):
                self.log(f"❌ Chat API返回的不是有效URL: {image_url}", "ERROR")
                self.save_test_result("Chat API", False, {"error": "返回的不是有效URL", "response": image_url})
                return False

            # 下载图片进行验证
            image_path = self.output_dir / "test_chat_api.png"
            if self.download_and_save_image(image_url, image_path):
                self.log(f"✅ Chat API图片已保存到: {image_path}")
                self.save_test_result("Chat API", True, {
                    "messages": messages,
                    "image_url": image_url,
                    "image_path": str(image_path)
                })
                return True
            else:
                self.log("❌ Chat API图片下载失败", "ERROR")
                self.save_test_result("Chat API", False, {"error": "图片下载失败", "image_url": image_url})
                return False
                
        except Exception as e:
            self.log(f"❌ Chat API测试失败: {str(e)}", "ERROR")
            self.save_test_result("Chat API", False, {"error": str(e)})
            return False
    
    def download_and_save_image(self, url: str, save_path: Path) -> bool:
        """下载并保存图片"""
        try:
            self.log(f"⬇️ 正在下载图片: {url}")
            
            image = download_image(url, timeout=60)
            if image is None:
                self.log("❌ 图片下载失败", "ERROR")
                return False
            
            # 保存图片
            image.save(save_path)
            file_size = save_path.stat().st_size / 1024 / 1024  # MB
            self.log(f"💾 图片已保存: {save_path} (大小: {file_size:.2f}MB)")
            
            return True
            
        except Exception as e:
            self.log(f"❌ 保存图片失败: {str(e)}", "ERROR")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        self.log("🚀 开始Flux-Kontext API完整测试")
        self.log("=" * 60)
        
        start_time = time.time()
        
        # 测试列表
        tests = [
            ("API密钥验证", self.test_api_key_validation),
            ("基础文生图", self.test_basic_text_to_image),
            ("图生图功能", self.test_image_to_image),
            ("多图参考", self.test_multi_image_reference),
            ("全参数测试", self.test_all_parameters),
            ("Chat API", self.test_chat_api),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            self.log(f"\n{'='*20} {test_name} {'='*20}")
            try:
                if test_func():
                    passed += 1
                    self.log(f"✅ {test_name} 通过")
                else:
                    failed += 1
                    self.log(f"❌ {test_name} 失败")
            except Exception as e:
                failed += 1
                self.log(f"❌ {test_name} 异常: {str(e)}", "ERROR")
            
            # 测试间隔
            time.sleep(1)
        
        # 生成测试报告
        end_time = time.time()
        duration = end_time - start_time
        
        self.log("\n" + "=" * 60)
        self.log("📊 测试完成！")
        self.log(f"⏱️ 总耗时: {duration:.2f}秒")
        self.log(f"✅ 通过: {passed}")
        self.log(f"❌ 失败: {failed}")
        self.log(f"📁 输出目录: {self.output_dir.absolute()}")
        
        # 保存测试报告
        self.save_test_report()
        
        return passed, failed
    
    def save_test_report(self):
        """保存测试报告"""
        report = {
            "test_summary": {
                "total_tests": len(self.test_results),
                "passed": sum(1 for r in self.test_results if r["success"]),
                "failed": sum(1 for r in self.test_results if not r["success"]),
                "timestamp": datetime.now().isoformat()
            },
            "test_results": self.test_results,
            "config": {
                "api_base_url": self.config.get_config("api_base_url"),
                "model": self.config.get_config("model"),
                "api_key_configured": self.config.is_api_key_valid()
            }
        }
        
        report_path = self.output_dir / "test_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        self.log(f"📄 测试报告已保存: {report_path}")

def main():
    """主函数"""
    print("🐰 Flux-Kontext API 完整测试工具")
    print("=" * 60)
    
    tester = FluxKontextTester()
    passed, failed = tester.run_all_tests()
    
    # 退出码
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    main() 