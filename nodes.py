"""
ComfyUI节点实现
定义Flux-Kontext图像生成节点
"""

import torch
from typing import Any, Tuple, Optional, Dict
from .api_client import FluxKontextAPI, FluxKontextAPIError
from .config import default_config
from .utils import download_image, pil_to_tensor, tensor_to_base64, format_error_message

class FluxKontextNode:
    """Flux-Kontext通用图像生成节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        """定义节点输入类型"""
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True,
                    "default": "A beautiful landscape painting",
                    "placeholder": "Enter image description prompt"
                }),
            },
            "optional": {
                "image": ("IMAGE",),
                "seed": ("INT", {
                    "default": 0, "min": 0, "max": 0xffffffffffffffff,
                    "step": 1, "display": "number"
                }),
                "guidance_scale": ("FLOAT", {
                    "default": 3.0, "min": 0.0, "max": 10.0, "step": 0.1,
                    "round": 0.01, "display": "slider"
                }),
                "num_inference_steps": ("INT", {
                    "default": 28, "min": 1, "max": 100, "step": 1,
                    "display": "slider"
                }),
                "aspect_ratio": (default_config.SUPPORTED_ASPECT_RATIOS, {
                    "default": "1:1"
                }),
                "output_format": (default_config.SUPPORTED_OUTPUT_FORMATS, {
                    "default": "jpeg"
                }),
                "safety_tolerance": ("INT", {
                    "default": 2, "min": 0, "max": 6, "step": 1,
                    "display": "slider"
                }),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
                "webhook_url": ("STRING", {"default": "", "placeholder": "Optional: Webhook URL"}),
                "webhook_secret": ("STRING", {"default": "", "placeholder": "Optional: Webhook Secret"}),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("image", "image_url", "status")
    FUNCTION = "execute"
    CATEGORY = "TuZi/Flux-Kontext"
    DESCRIPTION = "使用Flux-Kontext API生成高质量图像 (通用版)"
    
    def _create_error_result(self, error_message: str, original_image: Optional[torch.Tensor] = None) -> Dict[str, Any]:
        """创建一个包含错误信息的标准输出，如果可能则返回原始图像以避免工作流中断"""
        print(f"节点执行错误: {error_message}")
        # 如果有原始输入图像，就返回它，否则返回一个空的黑色图像
        if original_image is not None:
            image_out = original_image
        else:
            # 创建一个1x1的黑色图像作为占位符
            image_out = torch.zeros((1, 1, 3), dtype=torch.uint8)
            
        return {
            "ui": {"string": [error_message]},
            "result": (image_out, "N/A", f"失败: {error_message}")
        }

    def execute(self, 
                prompt: str,
                image: Optional[torch.Tensor] = None,
                seed: int = 0,
                guidance_scale: float = 3.0,
                num_inference_steps: int = 28,
                aspect_ratio: str = "1:1",
                output_format: str = "jpeg",
                safety_tolerance: int = 2,
                prompt_upsampling: bool = False,
                webhook_url: str = "",
                webhook_secret: str = "") -> Tuple[torch.Tensor, str, str]:
        """
        节点执行方法
        """
        # 从配置中获取API密钥
        api_key = default_config.get_api_key()

        # 检查API密钥是否存在
        if not api_key:
            return self._create_error_result(default_config.api_key_error_message, image)

        try:
            # 初始化API客户端
            api_client = FluxKontextAPI(api_key=api_key)
            
            # 4. 处理图像输入
            input_image_b64 = None
            status_mode = "文生图"
            if image is not None:
                input_image_b64 = tensor_to_base64(image, output_format)
                status_mode = "图生图"

            # 5. 准备API参数
            api_params = {
                "prompt": prompt,
                "input_image": input_image_b64,
                "seed": seed,
                "aspect_ratio": aspect_ratio,
                "output_format": output_format,
                "safety_tolerance": safety_tolerance,
                "prompt_upsampling": prompt_upsampling,
                "guidance_scale": guidance_scale,
                "num_inference_steps": num_inference_steps
            }
            if webhook_url.strip():
                api_params["webhook_url"] = webhook_url.strip()
            if webhook_secret.strip():
                api_params["webhook_secret"] = webhook_secret.strip()
            
            # 6. 调用API
            print(f"正在生成图像... 模式: {status_mode}, 提示词: {prompt[:80]}...")
            # 现在，api_client会直接返回一个 (PIL图像, URL) 的元组，或者抛出异常
            result_image_pil, result_image_url = api_client.generate_image(**api_params)
            
            # 7. 将PIL图像转换为Tensor
            result_image_tensor = pil_to_tensor(result_image_pil)
            
            # 8. 准备输出
            status_message = f"成功 | {status_mode} | {result_image_pil.width}x{result_image_pil.height}"
            
            return {
                "ui": {"string": [f"生成成功！\n图片URL: {result_image_url}\n状态: {status_message}"]},
                "result": (result_image_tensor, result_image_url, status_message)
            }

        except FluxKontextAPIError as e:
            # 直接显示来自API客户端的、清晰的错误信息
            return self._create_error_result(f"❌ API 调用失败: {str(e)}", image)
        except Exception as e:
            # 捕获其他意料之外的错误
            error_msg = format_error_message(e, "执行节点时发生未知错误")
            return self._create_error_result(error_msg, image)

# 注册节点到ComfyUI
NODE_CLASS_MAPPINGS = {
    "FluxKontextNode": FluxKontextNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxKontextNode": "🐰 Flux Kontext API"
} 