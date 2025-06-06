"""
ComfyUI-TuZi-Flux-Kontext 节点注册入口
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 导出节点映射，供ComfyUI识别
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 版本信息
__version__ = "1.0.0"

# 插件信息
WEB_DIRECTORY = "./web" 