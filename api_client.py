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
    from .utils import format_error_message
except ImportError:
    from config import FluxKontextConfig, default_config
    from utils import format_error_message

class FluxKontextAPIError(Exception):
    """API调用异常"""
    pass

class FluxKontextAPI:
    """Flux-Kontext API客户端类"""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[FluxKontextConfig] = None):
        """
        初始化API客户端
        
        Args:
            api_key: API密钥
            config: 配置对象
        """
        self.config = config or default_config
        if api_key:
            self.config.set_api_key(api_key)
        
        self.session = requests.Session()
        self._setup_session()
    
    def _setup_session(self):
        """设置HTTP会话"""
        self.session.headers.update({
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'ComfyUI-TuZi-Flux-Kontext/1.0'
        })
        
        # 设置API密钥
        api_key = self.config.get_api_key()
        if api_key:
            self.session.headers['Authorization'] = f'Bearer {api_key}'
    
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
                      seed: Optional[int] = None,
                      aspect_ratio: Optional[str] = None,
                      output_format: Optional[str] = None,
                      safety_tolerance: Optional[int] = None,
                      prompt_upsampling: Optional[bool] = None,
                      webhook_url: Optional[str] = None,
                      webhook_secret: Optional[str] = None) -> Dict[str, Any]:
        """
        生成图像（标准API）
        
        Args:
            prompt: 文本提示
            seed: 随机种子
            aspect_ratio: 宽高比
            output_format: 输出格式
            safety_tolerance: 安全容忍度
            prompt_upsampling: 提示上采样
            webhook_url: Webhook URL
            webhook_secret: Webhook密钥
            
        Returns:
            Dict: API响应，包含图像URL等信息
            
        Raises:
            FluxKontextAPIError: API调用失败
        """
        # 验证API密钥
        if not self.config.is_api_key_valid():
            raise FluxKontextAPIError("API密钥未设置或无效")
        
        # 构建请求数据
        payload = {
            "model": self.config.get_config('model'),
            "prompt": prompt
        }
        
        # 添加可选参数
        if seed is not None:
            payload["seed"] = seed
        
        if aspect_ratio is not None:
            if not self.config.validate_aspect_ratio(aspect_ratio):
                raise FluxKontextAPIError(f"不支持的宽高比: {aspect_ratio}")
            payload["aspect_ratio"] = aspect_ratio
        
        if output_format is not None:
            if not self.config.validate_output_format(output_format):
                raise FluxKontextAPIError(f"不支持的输出格式: {output_format}")
            payload["output_format"] = output_format
        
        if safety_tolerance is not None:
            if not self.config.validate_safety_tolerance(safety_tolerance):
                raise FluxKontextAPIError("安全容忍度必须在0-6之间")
            payload["safety_tolerance"] = safety_tolerance
        
        if prompt_upsampling is not None:
            payload["prompt_upsampling"] = prompt_upsampling
        
        if webhook_url is not None:
            payload["webhook_url"] = webhook_url
        
        if webhook_secret is not None:
            payload["webhook_secret"] = webhook_secret
        
        # 发送请求
        try:
            response = self._make_request('POST', '/v1/images/generations', payload)
            return response
        except Exception as e:
            raise FluxKontextAPIError(format_error_message(e, "图像生成"))
    
    def generate_image_chat(self, messages: List[Dict[str, str]]) -> str:
        """
        生成图像（Chat格式API）
        这个端点返回的不是标准JSON，而是一个包含Markdown图片链接的文本。
        
        Args:
            messages: 消息列表
            
        Returns:
            str: 提取到的图片URL，如果失败则返回错误信息
            
        Raises:
            FluxKontextAPIError: API调用失败
        """
        # 验证API密钥
        if not self.config.is_api_key_valid():
            raise FluxKontextAPIError("API密钥未设置或无效")
        
        payload = {
            "model": self.config.get_config('model'),
            "messages": messages,
            "stream": False  # 使用非流式获取完整响应
        }
        
        url = f"{self.config.get_config('api_base_url')}/v1/chat/completions"
        timeout = self.config.get_config('timeout', 300)
        
        try:
            response = self.session.post(url, json=payload, timeout=timeout)
            
            if response.status_code != 200:
                raise FluxKontextAPIError(f"Chat API请求失败: {response.status_code} - {response.text}")
            
            # 直接获取响应文本
            response_text = response.text
            
            # 使用正则表达式从Markdown链接中提取URL
            # ![...](URL)
            match = re.search(r'!\[.*?\]\((https?://[^\)]+)\)', response_text)
            
            if match:
                image_url = match.group(1)
                return image_url
            else:
                # 如果正则匹配失败，尝试寻找第一个http链接作为备用方案
                match_http = re.search(r'https?://[^\s"`<]+', response_text)
                if match_http:
                    return match_http.group(0)

                raise FluxKontextAPIError("在Chat API响应中未找到图片URL")
                
        except requests.exceptions.RequestException as e:
            raise FluxKontextAPIError(f"Chat API网络请求失败: {str(e)}")
        except Exception as e:
            raise FluxKontextAPIError(format_error_message(e, "Chat图像生成"))
    
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