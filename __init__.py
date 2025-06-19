"""
ComfyUI-TuZi-Flux-Kontext 节点注册入口
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 导出节点映射，供ComfyUI识别
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 版本信息 - 必须与 pyproject.toml 中的版本保持完全一致
__version__ = "1.0.7"

# 插件作者信息
__author__ = "ComfyUI-TuZi-Flux-Kontext Team"
__description__ = "兔子AI Flux-Kontext图像生成节点 - 支持文生图和图生图的高质量AI图像生成" 