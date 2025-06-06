"""
ComfyUI节点实现
定义Flux-Kontext图像生成节点
"""

import torch
import random
from typing import Any, Tuple, Optional, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
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
                "prompt": ("STRING", {"multiline": True, "default": ""}),
                "model": (["flux-kontext-pro", "flux-kontext-max"],),
                "num_images": ([1, 2, 4], {"default": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "guidance_scale": ("FLOAT", {"default": 3.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "aspect_ratio": (default_config.SUPPORTED_ASPECT_RATIOS,),
                "output_format": (default_config.SUPPORTED_OUTPUT_FORMATS,),
                "safety_tolerance": ("INT", {"default": 2, "min": 0, "max": 6}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image": ("IMAGE",),
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
                model: str,
                num_images: int,
                seed: int,
                guidance_scale: float,
                num_inference_steps: int,
                aspect_ratio: str,
                output_format: str,
                safety_tolerance: int,
                prompt_upsampling: bool,
                image: Optional[torch.Tensor] = None) -> Tuple[torch.Tensor, str, str]:
        """
        节点执行方法
        """
        api_key = default_config.get_api_key()
        if not api_key:
            return self._create_error_result(default_config.api_key_error_message, image)

        input_image_b64 = None
        status_mode = "文生图"
        if image is not None:
            input_image_b64 = tensor_to_base64(image, output_format)
            status_mode = "图生图"

        # --- 并发执行逻辑 ---
        results_pil = []
        result_urls = []
        errors = []

        def generate_single_image(current_seed):
            try:
                api_client = FluxKontextAPI(api_key=api_key)
                api_params = {
                    "prompt": prompt,
                    "model": model,
                    "input_image": input_image_b64,
                    "seed": current_seed,
                    "aspect_ratio": aspect_ratio,
                    "output_format": output_format,
                    "safety_tolerance": safety_tolerance,
                    "prompt_upsampling": prompt_upsampling,
                    "guidance_scale": guidance_scale,
                    "num_inference_steps": num_inference_steps
                }
                pil_image, url = api_client.generate_image(**api_params)
                return pil_image, url
            except Exception as e:
                return e

        with ThreadPoolExecutor(max_workers=min(num_images, 4)) as executor:
            # 使用初始种子或为每次迭代生成新种子
            seeds = [seed + i if seed != 0 else random.randint(0, 0xffffffffffffffff) for i in range(num_images)]
            
            future_to_seed = {executor.submit(generate_single_image, s): s for s in seeds}
            
            for future in as_completed(future_to_seed):
                try:
                    result = future.result()
                    if isinstance(result, Exception):
                        errors.append(f"种子 {future_to_seed[future]} 执行失败: {result}")
                    else:
                        pil_img, url = result
                        results_pil.append(pil_img)
                        result_urls.append(url)
                except Exception as exc:
                    errors.append(f"种子 {future_to_seed[future]} 执行时发生未知异常: {exc}")

        if not results_pil:
            error_summary = "\n".join(errors)
            return self._create_error_result(f"所有图像生成均失败。\n{error_summary}", image)

        # --- 处理成功的结果 ---
        result_image_tensor = pil_to_tensor(results_pil)
        
        # 准备输出信息
        success_count = len(results_pil)
        final_status = f"成功 {success_count}/{num_images} 张 | "
        if errors:
            final_status += f"失败 {len(errors)} 张: {'; '.join(errors)[:150]}..."
        
        final_urls = "\n".join(result_urls)
        
        return {
            "ui": {"string": [f"{final_status}\nURLs:\n{final_urls}"]},
            "result": (result_image_tensor, final_urls, final_status)
        }

# 注册节点到ComfyUI
NODE_CLASS_MAPPINGS = {
    "FluxKontextNode": FluxKontextNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxKontextNode": "🐰 Flux Kontext API"
} 