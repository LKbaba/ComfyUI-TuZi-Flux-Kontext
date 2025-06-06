"""
配置管理模块
处理API密钥、默认参数和环境变量
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path

class FluxKontextConfig:
    """Flux-Kontext配置管理类"""
    
    # 默认配置
    DEFAULT_CONFIG = {
        "api_base_url": "https://api.tu-zi.com",
        "model": "flux-kontext-pro",
        "aspect_ratio": "1:1",
        "output_format": "jpeg",
        "safety_tolerance": 2,
        "prompt_upsampling": False,
        "timeout": 300,
        "max_retries": 3
    }
    
    # 支持的宽高比
    SUPPORTED_ASPECT_RATIOS = [
        "21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "9:21"
    ]
    
    # 支持的输出格式
    SUPPORTED_OUTPUT_FORMATS = ["jpeg", "png"]
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化配置
        
        Args:
            api_key: API密钥，如果不提供则从环境变量读取
        """
        self.api_key = api_key or self._get_api_key_from_env()
        self.config = self.DEFAULT_CONFIG.copy()
    
    def _get_api_key_from_env(self) -> Optional[str]:
        """从环境变量或.env文件获取API密钥"""
        # 首先尝试从环境变量获取
        api_key = os.getenv("FLUX_KONTEXT_API_KEY") or os.getenv("TUZI_API_KEY")
        
        if api_key:
            return api_key
        
        # 如果环境变量中没有，尝试从.env文件读取
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if '=' in line:
                                key, value = line.split('=', 1)
                                key = key.strip()
                                value = value.strip()
                                if key in ["FLUX_KONTEXT_API_KEY", "TUZI_API_KEY"]:
                                    return value
            except Exception as e:
                print(f"读取.env文件失败: {e}")
        
        return None
    
    def get_api_key(self) -> Optional[str]:
        """获取API密钥"""
        return self.api_key
    
    def set_api_key(self, api_key: str):
        """设置API密钥"""
        self.api_key = api_key
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value: Any):
        """设置配置项"""
        self.config[key] = value
    
    def get_all_config(self) -> Dict[str, Any]:
        """获取所有配置"""
        return self.config.copy()
    
    def validate_aspect_ratio(self, aspect_ratio: str) -> bool:
        """验证宽高比是否支持"""
        return aspect_ratio in self.SUPPORTED_ASPECT_RATIOS
    
    def validate_output_format(self, output_format: str) -> bool:
        """验证输出格式是否支持"""
        return output_format in self.SUPPORTED_OUTPUT_FORMATS
    
    def validate_safety_tolerance(self, safety_tolerance: int) -> bool:
        """验证安全容忍度是否在有效范围内"""
        return 0 <= safety_tolerance <= 6
    
    def is_api_key_valid(self) -> bool:
        """检查API密钥是否有效（非空）"""
        return bool(self.api_key and self.api_key.strip())

# 全局配置实例
default_config = FluxKontextConfig() 