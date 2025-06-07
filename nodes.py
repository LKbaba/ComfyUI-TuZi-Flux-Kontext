"""
ComfyUI节点实现
定义Flux-Kontext图像生成节点
"""

import torch
import random
import os
import tempfile
from typing import Any, Tuple, Optional, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import fal_client
except ImportError:
    fal_client = None

from .api_client import FluxKontextAPI, FluxKontextAPIError
from .config import default_config
from .utils import download_image, pil_to_tensor, format_error_message, tensor_to_pil

class _FluxKontextNodeBase:
    """
    所有Flux-Kontext节点的内部基类，处理通用逻辑。
    """
    FUNCTION = "execute"
    CATEGORY = "TuZi/Flux.1 Kontext"

    @classmethod
    def IS_CHANGED(s, **kwargs):
        return float("NaN")

    def _create_error_result(self, error_message: str, original_image: Optional[torch.Tensor] = None) -> Dict[str, Any]:
        print(f"节点执行错误: {error_message}")
        if original_image is not None:
            image_out = original_image
        else:
            image_out = torch.zeros((1, 1, 1, 3), dtype=torch.float32)
            
        return {"ui": {"string": [error_message]}, "result": (image_out, f"失败: {error_message}")}

    def _execute_generation(self, tuzi_api_key: str, final_prompt: str, num_images: int, seed: int, model: str, **kwargs) -> Tuple[List[Any], List[str], List[str]]:
        results_pil, result_urls, errors = [], [], []

        def generate_single_image(current_seed):
            try:
                api_client = FluxKontextAPI(api_key=tuzi_api_key)
                api_params = {"prompt": final_prompt, "model": model, "seed": current_seed, **kwargs}
                pil_image, url = api_client.generate_image(**api_params)
                return pil_image, url
            except Exception as e:
                return e

        with ThreadPoolExecutor(max_workers=min(num_images, 4)) as executor:
            seeds = [seed + i if seed != 0 else random.randint(0, 0xffffffffffffffff) for i in range(num_images)]
            future_to_seed = {executor.submit(generate_single_image, s): s for s in seeds}
            
            for future in as_completed(future_to_seed):
                try:
                    result = future.result()
                    if isinstance(result, Exception):
                        errors.append(f"Seed {future_to_seed[future]} failed: {result}")
                    else:
                        pil_img, url = result
                        results_pil.append(pil_img)
                        result_urls.append(url)
                except Exception as exc:
                    errors.append(f"Seed {future_to_seed[future]} raised an exception: {exc}")
        
        return results_pil, result_urls, errors

# 节点1: 文生图
class FluxKontext_TextToImage(_FluxKontextNodeBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": 'Extreme close-up of a single tiger eye, direct frontal view. Detailed iris and pupil. Sharp focus on eye texture and color. Natural lighting to capture authentic eye shine and depth. The word "FLUX" is painted over it in big, white brush strokes with visible texture.'}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-max"}),
                "num_images": ([1, 2, 4], {"default": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 10.0, "step": 0.1}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "aspect_ratio": (default_config.SUPPORTED_ASPECT_RATIOS, {"default": "1:1"}),
                "output_format": (default_config.SUPPORTED_OUTPUT_FORMATS, {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 3, "min": 0, "max": 6}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status")

    def execute(self, **kwargs):
        tuzi_api_key = default_config.get_api_key()
        if not tuzi_api_key:
            return self._create_error_result(default_config.api_key_error_message)

        num_images = kwargs.pop("num_images")
        seed = kwargs.pop("seed")
        final_prompt = kwargs.pop("prompt")
        model = kwargs.pop("model")
        
        results_pil, result_urls, errors = self._execute_generation(tuzi_api_key, final_prompt, num_images, seed, model, **kwargs)

        if not results_pil:
            return self._create_error_result(f"All image generations failed.\n{'; '.join(errors)}")

        success_count = len(results_pil)
        final_status = f"Mode: Text-to-Image | Success: {success_count}/{num_images}"
        if errors:
            final_status += f" | Failed: {len(errors)}"
        final_status += f"\nURLs:\n" + "\n".join(result_urls)
        
        return {"ui": {"string": [final_status]}, "result": (pil_to_tensor(results_pil), final_status)}

# 节点2: 图生图 (单图)
class FluxKontext_ImageToImage(_FluxKontextNodeBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "The character is sitting cross-legged on the sofa, and the Dalmatian is lying on the blanket sleeping."}),
                "model": (["flux-kontext-max"],),
                "num_images": ([1, 2, 4], {"default": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 10.0, "step": 0.1}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "aspect_ratio": (default_config.SUPPORTED_ASPECT_RATIOS, {"default": "1:1"}),
                "output_format": (default_config.SUPPORTED_OUTPUT_FORMATS, {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 3, "min": 0, "max": 6}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status")
    
    def execute(self, image: torch.Tensor, **kwargs):
        tuzi_api_key = default_config.get_api_key()
        if not tuzi_api_key:
            return self._create_error_result(default_config.api_key_error_message, image)

        if fal_client is None:
            return self._create_error_result("Error: 'fal-client' not installed. Please run pip install -r requirements.txt", image)

        fal_key = default_config.get_fal_key()
        if not fal_key:
            return self._create_error_result(default_config.fal_key_error_message, image)
        
        os.environ['FAL_KEY'] = fal_key
        temp_file_path = None
        try:
            pil_images = tensor_to_pil(image)
            if not pil_images:
                return self._create_error_result("Cannot convert input image.", image)
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                pil_images[0].save(temp_file, 'PNG')
                temp_file_path = temp_file.name
            
            uploaded_url = fal_client.upload_file(temp_file_path)
            final_prompt = f"{uploaded_url} {kwargs['prompt']}"

        except Exception as e:
            return self._create_error_result(f"Image-to-Image preparation failed: {format_error_message(e)}", image)
        finally:
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

        num_images = kwargs.pop("num_images")
        seed = kwargs.pop("seed")
        model = kwargs.pop("model")
        kwargs.pop("prompt")
        
        results_pil, result_urls, errors = self._execute_generation(tuzi_api_key, final_prompt, num_images, seed, model, **kwargs)
        
        if not results_pil:
            return self._create_error_result(f"All image generations failed.\n{'; '.join(errors)}", image)

        success_count = len(results_pil)
        final_status = f"Mode: Image-to-Image | Success: {success_count}/{num_images}"
        if errors:
            final_status += f" | Failed: {len(errors)}"
        final_status += f"\nReference URL: {uploaded_url}\nResult URLs:\n" + "\n".join(result_urls)
        
        return {"ui": {"string": [final_status]}, "result": (pil_to_tensor(results_pil), final_status)}

# 节点3: 多图生图
class FluxKontext_MultiImageToImage(_FluxKontextNodeBase):
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "The character is sitting cross-legged on the sofa, and the Dalmatian is lying on the blanket sleeping."}),
                "model": (["flux-kontext-pro", "flux-kontext-max"], {"default": "flux-kontext-max"}),
                "num_images": ([1, 2, 4], {"default": 1}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "guidance_scale": ("FLOAT", {"default": 3.5, "min": 0.0, "max": 10.0, "step": 0.1}),
                "num_inference_steps": ("INT", {"default": 28, "min": 1, "max": 100}),
                "aspect_ratio": (default_config.SUPPORTED_ASPECT_RATIOS, {"default": "1:1"}),
                "output_format": (default_config.SUPPORTED_OUTPUT_FORMATS, {"default": "png"}),
                "safety_tolerance": ("INT", {"default": 3, "min": 0, "max": 6}),
                "prompt_upsampling": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
            }
        }
        
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status")

    def execute(self, **kwargs):
        images_in = [kwargs.get(f"image_{i}") for i in range(1, 5) if kwargs.get(f"image_{i}") is not None]
        
        if not images_in:
            return self._create_error_result("Error: Multi-Image node requires at least one image input.")

        tuzi_api_key = default_config.get_api_key()
        if not tuzi_api_key:
            return self._create_error_result(default_config.api_key_error_message)

        fal_key = default_config.get_fal_key()
        if not fal_key:
            return self._create_error_result(default_config.fal_key_error_message)
        
        os.environ['FAL_KEY'] = fal_key
        
        uploaded_urls = []
        temp_files = []
        try:
            for i, image_tensor in enumerate(images_in):
                pil_images = tensor_to_pil(image_tensor)
                if not pil_images: continue

                with tempfile.NamedTemporaryFile(suffix=f'_{i}.png', delete=False) as temp_file:
                    pil_images[0].save(temp_file, 'PNG')
                    temp_files.append(temp_file.name)
                
                uploaded_urls.append(fal_client.upload_file(temp_files[-1]))
            
            if not uploaded_urls:
                return self._create_error_result("All input images could not be processed or uploaded.")

            url_prefix = " ".join(uploaded_urls)
            final_prompt = f"{url_prefix} {kwargs['prompt']}"

        except Exception as e:
            return self._create_error_result(f"Multi-Image upload failed: {format_error_message(e)}")
        finally:
            for path in temp_files:
                if os.path.exists(path):
                    os.unlink(path)
        
        num_images = kwargs.pop("num_images")
        seed = kwargs.pop("seed")
        model = kwargs.pop("model")
        kwargs.pop("prompt")
        for i in range(1, 5): kwargs.pop(f"image_{i}", None)
        
        results_pil, result_urls, errors = self._execute_generation(tuzi_api_key, final_prompt, num_images, seed, model, **kwargs)
        
        if not results_pil:
            return self._create_error_result(f"All image generations failed.\n{'; '.join(errors)}")

        success_count = len(results_pil)
        final_status = f"Mode: Multi-Image ({len(uploaded_urls)} refs) | Success: {success_count}/{num_images}"
        if errors:
            final_status += f" | Failed: {len(errors)}"
        final_status += f"\nReference URLs:\n" + "\n".join(uploaded_urls)
        final_status += f"\nResult URLs:\n" + "\n".join(result_urls)

        return {"ui": {"string": [final_status]}, "result": (pil_to_tensor(results_pil), final_status)}


NODE_CLASS_MAPPINGS = {
    "FluxKontext_TextToImage": FluxKontext_TextToImage,
    "FluxKontext_ImageToImage": FluxKontext_ImageToImage,
    "FluxKontext_MultiImageToImage": FluxKontext_MultiImageToImage,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxKontext_TextToImage": "🐰Flux.1 Kontext - Text to Image",
    "FluxKontext_ImageToImage": "🐰Flux.1 Kontext - Editing",
    "FluxKontext_MultiImageToImage": "🐰Flux.1 Kontext - Editing (Multi Image)",
} 