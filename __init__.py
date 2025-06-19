"""
ComfyUI-TuZi-Flux-Kontext 节点注册入口
"""

from .nodes import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

# 导出节点映射，供ComfyUI识别
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# 动态获取版本信息，确保与pyproject.toml保持一致
try:
    # Python 3.8+ 推荐使用 importlib.metadata
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("ComfyUI-TuZi-Flux-Kontext")
    except PackageNotFoundError:
        # 如果包未正式安装，回退到固定版本号
        __version__ = "1.0.3"
except ImportError:
    # Python < 3.8 的兼容性处理
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution("ComfyUI-TuZi-Flux-Kontext").version
    except:
        # 最终回退
        __version__ = "1.0.3"

# 插件作者信息
__author__ = "ComfyUI-TuZi-Flux-Kontext Team"
__description__ = "兔子AI Flux-Kontext图像生成节点 - 支持文生图和图生图的高质量AI图像生成" 