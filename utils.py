"""
工具函数模块
提供图像处理、URL解析、数据转换等通用功能
"""

import io
import requests
import numpy as np
from PIL import Image
from typing import Optional, Union, List, Tuple
import torch
import re
from urllib.parse import urlparse

def download_image(url: str, timeout: int = 30) -> Optional[Image.Image]:
    """
    从URL下载图像
    
    Args:
        url: 图像URL
        timeout: 超时时间（秒）
        
    Returns:
        PIL.Image对象，如果下载失败返回None
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        image = Image.open(io.BytesIO(response.content))
        return image
    except Exception as e:
        print(f"下载图像失败: {url}, 错误: {str(e)}")
        return None

def pil_to_tensor(image: Image.Image) -> torch.Tensor:
    """
    将PIL图像转换为ComfyUI张量格式
    
    Args:
        image: PIL图像对象
        
    Returns:
        torch.Tensor: 形状为 [1, H, W, 3] 的张量，值范围 [0, 1]
    """
    # 确保图像是RGB格式
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # 转换为numpy数组
    image_array = np.array(image).astype(np.float32) / 255.0
    
    # 转换为torch张量并调整维度 [H, W, C] -> [1, H, W, C]
    tensor = torch.from_numpy(image_array).unsqueeze(0)
    
    return tensor

def tensor_to_pil(tensor: torch.Tensor) -> Image.Image:
    """
    将ComfyUI张量转换为PIL图像
    
    Args:
        tensor: 形状为 [1, H, W, 3] 或 [H, W, 3] 的张量
        
    Returns:
        PIL.Image对象
    """
    # 如果是4维张量，取第一个
    if tensor.dim() == 4:
        tensor = tensor.squeeze(0)
    
    # 确保值在[0, 1]范围内
    tensor = torch.clamp(tensor, 0, 1)
    
    # 转换为numpy数组并缩放到[0, 255]
    image_array = (tensor.cpu().numpy() * 255).astype(np.uint8)
    
    # 创建PIL图像
    image = Image.fromarray(image_array, 'RGB')
    
    return image

def validate_url(url: str) -> bool:
    """
    验证URL是否有效
    
    Args:
        url: 要验证的URL
        
    Returns:
        bool: URL是否有效
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def parse_image_urls(prompt: str) -> Tuple[List[str], str]:
    """
    从提示词中解析图像URL
    
    Args:
        prompt: 包含URL的提示词
        
    Returns:
        Tuple[List[str], str]: (URL列表, 清理后的提示词)
    """
    # 匹配HTTP/HTTPS URL的正则表达式
    url_pattern = r'https?://[^\s]+'
    
    # 找到所有URL
    urls = re.findall(url_pattern, prompt)
    
    # 从提示词中移除URL
    clean_prompt = re.sub(url_pattern, '', prompt).strip()
    
    # 清理多余的空格
    clean_prompt = re.sub(r'\s+', ' ', clean_prompt)
    
    return urls, clean_prompt

def validate_aspect_ratio(aspect_ratio: str) -> bool:
    """
    验证宽高比格式是否正确
    
    Args:
        aspect_ratio: 宽高比字符串，如 "16:9"
        
    Returns:
        bool: 格式是否正确
    """
    pattern = r'^\d+:\d+$'
    return bool(re.match(pattern, aspect_ratio))

def calculate_dimensions(aspect_ratio: str, base_size: int = 1024) -> Tuple[int, int]:
    """
    根据宽高比计算图像尺寸
    
    Args:
        aspect_ratio: 宽高比字符串，如 "16:9"
        base_size: 基础尺寸
        
    Returns:
        Tuple[int, int]: (宽度, 高度)
    """
    try:
        width_ratio, height_ratio = map(int, aspect_ratio.split(':'))
        
        # 计算实际尺寸，保持总像素数接近base_size^2
        total_ratio = width_ratio * height_ratio
        scale = (base_size * base_size / total_ratio) ** 0.5
        
        width = int(width_ratio * scale)
        height = int(height_ratio * scale)
        
        # 确保尺寸是8的倍数（AI模型通常需要）
        width = (width // 8) * 8
        height = (height // 8) * 8
        
        return width, height
    except:
        return base_size, base_size

def format_error_message(error: Exception, context: str = "") -> str:
    """
    格式化错误消息，提供用户友好的错误信息
    
    Args:
        error: 异常对象
        context: 错误上下文
        
    Returns:
        str: 格式化的错误消息
    """
    error_type = type(error).__name__
    error_msg = str(error)
    
    if context:
        return f"[{context}] {error_type}: {error_msg}"
    else:
        return f"{error_type}: {error_msg}"

def safe_filename(filename: str) -> str:
    """
    生成安全的文件名，移除特殊字符
    
    Args:
        filename: 原始文件名
        
    Returns:
        str: 安全的文件名
    """
    # 移除或替换不安全的字符
    safe_chars = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # 限制长度
    if len(safe_chars) > 100:
        safe_chars = safe_chars[:100]
    
    return safe_chars

def bytes_to_mb(bytes_size: int) -> float:
    """
    将字节转换为MB
    
    Args:
        bytes_size: 字节大小
        
    Returns:
        float: MB大小
    """
    return bytes_size / (1024 * 1024) 