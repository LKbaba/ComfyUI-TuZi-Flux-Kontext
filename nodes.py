"""
ComfyUI节点实现
定义Flux-Kontext图像生成节点
"""

import torch
from typing import Dict, Any, Tuple, Optional
from api_client import FluxKontextAPI, FluxKontextAPIError
from config import FluxKontextConfig
from utils import download_image, pil_to_tensor, parse_image_urls, format_error_message

class FluxKontextNode:
    """Flux-Kontext图像生成节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入类型"""
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "一只可爱的猫咪",
                    "placeholder": "输入图像描述提示词，可以包含图片URL"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "输入您的API密钥"
                }),
            },
            "optional": {
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647,
                    "step": 1,
                    "display": "number"
                }),
                "aspect_ratio": (["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"], {
                    "default": "1:1"
                }),
                "output_format": (["jpeg", "png"], {
                    "default": "jpeg"
                }),
                "safety_tolerance": ("INT", {
                    "default": 2,
                    "min": 0,
                    "max": 6,
                    "step": 1,
                    "display": "slider"
                }),
                "prompt_upsampling": ("BOOLEAN", {
                    "default": False
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "image_url", "status")
    FUNCTION = "generate_image"
    CATEGORY = "TuZi/Flux-Kontext"
    DESCRIPTION = "使用Flux-Kontext API生成高质量图像"
    
    def generate_image(self, 
                      prompt: str,
                      api_key: str,
                      seed: int = -1,
                      aspect_ratio: str = "1:1",
                      output_format: str = "jpeg",
                      safety_tolerance: int = 2,
                      prompt_upsampling: bool = False) -> Tuple[torch.Tensor, str, str]:
        """
        生成图像的主要方法
        
        Args:
            prompt: 提示词
            api_key: API密钥
            seed: 随机种子
            aspect_ratio: 宽高比
            output_format: 输出格式
            safety_tolerance: 安全容忍度
            prompt_upsampling: 提示上采样
            
        Returns:
            Tuple[torch.Tensor, str, str]: (图像张量, 图像URL, 状态信息)
        """
        try:
            # 验证API密钥
            if not api_key or not api_key.strip():
                return self._create_error_result("请提供有效的API密钥")
            
            # 验证提示词
            if not prompt or not prompt.strip():
                return self._create_error_result("请提供有效的提示词")
            
            # 解析提示词中的图片URL
            urls, clean_prompt = parse_image_urls(prompt)
            if urls:
                # 如果有URL，保持原始格式（URL + 描述）
                final_prompt = prompt
                status_msg = f"检测到 {len(urls)} 个图片URL"
            else:
                final_prompt = clean_prompt
                status_msg = "纯文本提示词"
            
            # 创建API客户端
            config = FluxKontextConfig(api_key=api_key)
            api_client = FluxKontextAPI(config=config)
            
            # 准备API参数
            api_params = {
                "prompt": final_prompt,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
                "safety_tolerance": safety_tolerance,
                "prompt_upsampling": prompt_upsampling
            }
            
            # 处理种子参数
            if seed >= 0:
                api_params["seed"] = seed
            
            # 调用API生成图像
            print(f"正在生成图像... 提示词: {final_prompt[:50]}...")
            response = api_client.generate_image(**api_params)
            
            # 解析响应
            if "data" in response and len(response["data"]) > 0:
                image_url = response["data"][0]["url"]
                
                # 下载图像
                print(f"正在下载图像: {image_url}")
                pil_image = download_image(image_url)
                
                if pil_image is None:
                    return self._create_error_result("图像下载失败")
                
                # 转换为ComfyUI张量格式
                image_tensor = pil_to_tensor(pil_image)
                
                success_msg = f"✅ 图像生成成功 | {status_msg} | 尺寸: {pil_image.size}"
                return (image_tensor, image_url, success_msg)
            else:
                return self._create_error_result("API响应中没有图像数据")
                
        except FluxKontextAPIError as e:
            error_msg = f"❌ API错误: {str(e)}"
            print(error_msg)
            return self._create_error_result(error_msg)
        except Exception as e:
            error_msg = f"❌ 未知错误: {format_error_message(e)}"
            print(error_msg)
            return self._create_error_result(error_msg)
    
    def _create_error_result(self, error_message: str) -> Tuple[torch.Tensor, str, str]:
        """
        创建错误结果
        
        Args:
            error_message: 错误消息
            
        Returns:
            Tuple: 包含空图像的错误结果
        """
        # 创建一个空的黑色图像
        empty_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
        return (empty_image, "", error_message)

class FluxKontextAdvancedNode:
    """Flux-Kontext高级节点，支持更多参数"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入类型"""
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "一只可爱的猫咪",
                    "placeholder": "输入图像描述提示词，可以包含图片URL"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "输入您的API密钥"
                }),
            },
            "optional": {
                "seed": ("INT", {
                    "default": -1,
                    "min": -1,
                    "max": 2147483647,
                    "step": 1
                }),
                "aspect_ratio": (["1:1", "16:9", "9:16", "4:3", "3:4", "21:9", "9:21"], {
                    "default": "1:1"
                }),
                "output_format": (["jpeg", "png"], {
                    "default": "jpeg"
                }),
                "safety_tolerance": ("INT", {
                    "default": 2,
                    "min": 0,
                    "max": 6,
                    "step": 1
                }),
                "prompt_upsampling": ("BOOLEAN", {
                    "default": False
                }),
                "webhook_url": ("STRING", {
                    "default": "",
                    "placeholder": "可选：Webhook通知URL"
                }),
                "webhook_secret": ("STRING", {
                    "default": "",
                    "placeholder": "可选：Webhook签名密钥"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("image", "image_url", "response_data", "status")
    FUNCTION = "generate_image_advanced"
    CATEGORY = "TuZi/Flux-Kontext"
    DESCRIPTION = "Flux-Kontext高级图像生成，支持Webhook等高级功能"
    
    def generate_image_advanced(self, 
                               prompt: str,
                               api_key: str,
                               seed: int = -1,
                               aspect_ratio: str = "1:1",
                               output_format: str = "jpeg",
                               safety_tolerance: int = 2,
                               prompt_upsampling: bool = False,
                               webhook_url: str = "",
                               webhook_secret: str = "") -> Tuple[torch.Tensor, str, str, str]:
        """
        高级图像生成方法，支持更多参数
        
        Returns:
            Tuple[torch.Tensor, str, str, str]: (图像张量, 图像URL, 响应数据, 状态信息)
        """
        try:
            # 验证API密钥
            if not api_key or not api_key.strip():
                return self._create_error_result("请提供有效的API密钥")
            
            # 验证提示词
            if not prompt or not prompt.strip():
                return self._create_error_result("请提供有效的提示词")
            
            # 解析提示词中的图片URL
            urls, clean_prompt = parse_image_urls(prompt)
            if urls:
                final_prompt = prompt
                status_msg = f"检测到 {len(urls)} 个图片URL"
            else:
                final_prompt = clean_prompt
                status_msg = "纯文本提示词"
            
            # 创建API客户端
            config = FluxKontextConfig(api_key=api_key)
            api_client = FluxKontextAPI(config=config)
            
            # 准备API参数
            api_params = {
                "prompt": final_prompt,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
                "safety_tolerance": safety_tolerance,
                "prompt_upsampling": prompt_upsampling
            }
            
            # 处理种子参数
            if seed >= 0:
                api_params["seed"] = seed
            
            # 处理Webhook参数
            if webhook_url and webhook_url.strip():
                api_params["webhook_url"] = webhook_url.strip()
                if webhook_secret and webhook_secret.strip():
                    api_params["webhook_secret"] = webhook_secret.strip()
            
            # 调用API生成图像
            print(f"正在生成图像... 提示词: {final_prompt[:50]}...")
            response = api_client.generate_image(**api_params)
            
            # 转换响应为JSON字符串
            response_json = str(response)
            
            # 解析响应
            if "data" in response and len(response["data"]) > 0:
                image_url = response["data"][0]["url"]
                
                # 下载图像
                print(f"正在下载图像: {image_url}")
                pil_image = download_image(image_url)
                
                if pil_image is None:
                    return self._create_error_result("图像下载失败")
                
                # 转换为ComfyUI张量格式
                image_tensor = pil_to_tensor(pil_image)
                
                success_msg = f"✅ 图像生成成功 | {status_msg} | 尺寸: {pil_image.size}"
                return (image_tensor, image_url, response_json, success_msg)
            else:
                return self._create_error_result("API响应中没有图像数据")
                
        except FluxKontextAPIError as e:
            error_msg = f"❌ API错误: {str(e)}"
            print(error_msg)
            return self._create_error_result(error_msg)
        except Exception as e:
            error_msg = f"❌ 未知错误: {format_error_message(e)}"
            print(error_msg)
            return self._create_error_result(error_msg)
    
    def _create_error_result(self, error_message: str) -> Tuple[torch.Tensor, str, str, str]:
        """
        创建错误结果
        
        Args:
            error_message: 错误消息
            
        Returns:
            Tuple: 包含空图像的错误结果
        """
        # 创建一个空的黑色图像
        empty_image = torch.zeros((1, 512, 512, 3), dtype=torch.float32)
        return (empty_image, "", "", error_message) 