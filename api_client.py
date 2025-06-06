"""
Flux-Kontext API客户端
封装与api.tu-zi.com的所有交互逻辑
"""

import json
import time
import requests
import re
from typing import Optional, Dict, Any, List
try:
    from .config import FluxKontextConfig, default_config
    from .utils import format_error_message, download_image
except ImportError:
    from config import FluxKontextConfig, default_config
    from utils import format_error_message, download_image

class FluxKontextAPIError(Exception):
    """API调用异常"""
    pass

class FluxKontextAPI:
    """Flux-Kontext API客户端类"""
    
    def __init__(self, api_key: str, config: Optional[FluxKontextConfig] = None):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥
            config: 配置对象
        """
        if not api_key or not api_key.strip():
            raise FluxKontextAPIError("API密钥在初始化时不能为空")
            
        self.api_key = api_key
        self.config = config or default_config
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """设置HTTP会话"""
        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'ComfyUI-TuZi-Flux-Kontext/1.0'
        })
        
        # 直接使用传入的API密钥设置认证头
        self.session.headers['Authorization'] = f'Bearer {self.api_key}'
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None, 
                     timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        发送HTTP请求
        
        Args:
            method: HTTP方法
            endpoint: API端点
            data: 请求数据
            timeout: 超时时间
            
        Returns:
            Dict: API响应数据
            
        Raises:
            FluxKontextAPIError: API调用失败
        """
        url = f"{self.config.get_config('api_base_url')}{endpoint}"
        timeout = timeout or self.config.get_config('timeout', 300)
        max_retries = self.config.get_config('max_retries', 3)
        
        for attempt in range(max_retries):
            try:
                if method.upper() == 'POST':
                    response = self.session.post(
                        url, 
                        json=data, 
                        timeout=timeout
                    )
                else:
                    response = self.session.get(url, timeout=timeout)
                
                # 检查HTTP状态码
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 401:
                    raise FluxKontextAPIError("API密钥无效或已过期")
                elif response.status_code == 429:
                    raise FluxKontextAPIError("请求频率过高，请稍后重试")
                elif response.status_code >= 500:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # 指数退避
                        continue
                    raise FluxKontextAPIError(f"服务器错误: {response.status_code}")
                else:
                    error_msg = f"API请求失败: {response.status_code}"
                    try:
                        error_data = response.json()
                        if 'error' in error_data:
                            error_msg += f" - {error_data['error']}"
                    except:
                        pass
                    raise FluxKontextAPIError(error_msg)
                    
            except requests.exceptions.Timeout:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise FluxKontextAPIError("请求超时，请检查网络连接")
            except requests.exceptions.ConnectionError:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise FluxKontextAPIError("网络连接失败，请检查网络设置")
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise FluxKontextAPIError(format_error_message(e, "网络请求"))
        
        raise FluxKontextAPIError("达到最大重试次数，请求失败")
    
    def generate_image(self, 
                      prompt: str,
                      model: str = "flux-kontext-pro",
                      input_image: Optional[str] = None,
                      seed: Optional[int] = None,
                      aspect_ratio: Optional[str] = None,
                      output_format: Optional[str] = None,
                      safety_tolerance: Optional[int] = None,
                      prompt_upsampling: Optional[bool] = None,
                      guidance_scale: Optional[float] = None,
                      num_inference_steps: Optional[int] = None,
                      webhook_url: Optional[str] = None,
                      webhook_secret: Optional[str] = None) -> Dict[str, Any]:
        """
        生成图像（标准API）
        
        Args:
            prompt: 文本提示
            model: 模型名称
            input_image: Base64编码的输入图像
            seed: 随机种子
            aspect_ratio: 宽高比
            output_format: 输出格式
            safety_tolerance: 安全容忍度
            prompt_upsampling: 提示上采样
            guidance_scale: 指导强度
            num_inference_steps: 推理步数
            webhook_url: Webhook URL
            webhook_secret: Webhook密钥
            
        Returns:
            Dict: API响应，包含图像URL等信息
            
        Raises:
            FluxKontextAPIError: API调用失败
        """
        # 构建请求数据
        payload = {
            "model": model,
            "prompt": prompt
        }
        
        # 动态添加所有非空的可选参数
        # 这种方式更简洁且易于维护
        optional_params = {
            "input_image": input_image,
            "seed": seed,
            "aspect_ratio": aspect_ratio,
            "output_format": output_format,
            "safety_tolerance": safety_tolerance,
            "prompt_upsampling": prompt_upsampling,
            "guidance_scale": guidance_scale,
            "num_inference_steps": num_inference_steps,
            "webhook_url": webhook_url,
            "webhook_secret": webhook_secret,
        }

        for key, value in optional_params.items():
            # 只有当值不是None，或者对于字符串，不是空字符串时，才添加到payload
            if value is not None and value != '':
                payload[key] = value

        # 发送请求
        try:
            response = self._make_request('POST', '/v1/images/generations', data=payload)
        except Exception as e:
            # 确保将所有底层异常统一包装成我们的自定义异常
            if isinstance(e, FluxKontextAPIError):
                raise e
            raise FluxKontextAPIError(format_error_message(e, "图像生成"))

        # 检查响应结构，提取图像URL或错误信息
        # 这一步是关键，确保我们能处理API的正常响应和各种错误情况
        if 'data' in response and isinstance(response['data'], list) and len(response['data']) > 0 and 'url' in response['data'][0]:
            image_url = response['data'][0]['url']
            if not isinstance(image_url, str) or not image_url.startswith('http'):
                 raise FluxKontextAPIError(f"API返回了无效的图片URL格式: {str(image_url)[:100]}")
            
            try:
                # 下载图像
                print(f"⬇️ 正在从 {image_url} 下载图像...")
                timeout = self.config.get_config('timeout', 60) # 提供一个默认值
                pil_image = download_image(image_url, timeout=timeout)
                if pil_image is None:
                    # 这里的错误信息可以更具体
                    raise FluxKontextAPIError(f"从URL下载图片失败 (可能是网络超时或链接已失效): {image_url}")
                
                print("✅ 图像下载并处理成功")
                # 直接返回PIL图像和URL，这是与之前最大的不同
                return pil_image, image_url

            except Exception as e:
                raise FluxKontextAPIError(f"下载或处理图像时出错: {str(e)}")
        else:
            # 如果响应中没有预期的图像数据，则尝试解析并抛出详细的错误信息
            error_message = response.get("error", {}).get("message", "API返回未知格式的响应")
            raise FluxKontextAPIError(f"API错误: {error_message} | 原始响应: {str(response)[:200]}")
    
    def test_connection(self) -> bool:
        """
        测试API连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            # 尝试一个简单的请求来测试连接
            self.generate_image("test", seed=1)
            return True
        except:
            return False
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        获取API状态信息
        
        Returns:
            Dict: 状态信息
        """
        status = {
            "api_key_valid": self.config.is_api_key_valid(),
            "base_url": self.config.get_config('api_base_url'),
            "model": self.config.get_config('model'),
            "timeout": self.config.get_config('timeout'),
            "max_retries": self.config.get_config('max_retries')
        }
        
        # 测试连接
        try:
            status["connection_ok"] = self.test_connection()
        except:
            status["connection_ok"] = False
        
        return status 