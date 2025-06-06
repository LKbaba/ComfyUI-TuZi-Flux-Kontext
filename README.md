# ComfyUI-TuZi-Flux-Kontext

🐰 **Flux-Kontext Pro** 的 ComfyUI 自定义节点，使用官方标准API，支持文生图和图生图。

## ✨ 特性

- 🎨 **高质量图像生成** - 基于 Flux-Kontext-Pro 模型，支持文生图和图生图。
- ⚙️ **丰富的参数控制** - 支持调整指导强度(Guidance)、推理步数(Steps)、宽高比、种子等核心参数。
- 🔑 **专业的密钥管理** - 通过 `.env` 文件或环境变量配置API密钥，安全且方便。
- 🛡️ **健壮的错误处理** - 在API密钥未配置时提供清晰的中文指引，并在节点执行失败时尽量维持工作流不中断。
- 🔧 **统一的全功能节点** - 将所有功能集成于一个节点，简洁易用。

## 📦 安装

1.  打开您的ComfyUI安装目录。
2.  进入 `custom_nodes` 文件夹。
3.  通过 `git` 克隆本项目:
    ```bash
    cd ComfyUI/custom_nodes/
    git clone https://github.com/your-username/ComfyUI-TuZi-Flux-Kontext.git
    ```
4.  安装依赖:
    ```bash
    cd ComfyUI-TuZi-Flux-Kontext
    pip install -r requirements.txt
    ```
5.  重启ComfyUI。

## 🔑 API 密钥设置

为了使用本节点，您需要配置您的兔子AI API密钥。我们推荐使用 `.env` 文件的方式。

1.  **获取密钥**: 访问 [兔子AI官网](https://tu-zi.com) 并登录，在控制台获取您的 API 密钥。

2.  **配置密钥**:
    -   在 `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/` 目录下，创建一个名为 `.env` 的文件。
    -   在该文件中，添加以下内容，并将 `your-api-key-here` 替换为您真实的密钥:
        ```
        TUZI_API_KEY=your-api-key-here
        ```
    -   保存文件并重启ComfyUI。

*或者，您也可以通过设置名为 `TUZI_API_KEY` 的系统环境变量来配置密钥。*

如果未正确配置密钥，节点将显示红色的错误信息，并提供详细的中文设置指引。

## 🚀 使用方法

在ComfyUI中，添加 `🐰 Flux Kontext API` 节点 (位于 `TuZi/Flux-Kontext` 分类下)。

### 输入参数

-   **`prompt`**: 图像的文本描述。
-   **`image` (可选)**: 连接一个图像输入，即可启用**图生图**模式。
-   **`seed`**: 随机种子。
-   **`control_after_generate`**: 控制种子在每次生成后是否变化 (固定/递增/随机)。
-   **`guidance_scale`**: 指导强度。数值越高，图像与提示词的关联性越强。
-   **`num_inference_steps`**: 推理步数。步数越多，细节可能越丰富，但生成时间也越长。
-   **`aspect_ratio`**: 预设的图像宽高比。
-   **`output_format`**: 输出图像的格式 (jpeg/png)。
-   **`safety_tolerance`**: 内容安全容忍度 (0-6)。
-   **`prompt_upsampling`**: 是否启用提示词增强。
-   **`webhook_url` (可选)**: 用于接收生成结果的Webhook URL。
-   **`webhook_secret` (可选)**: Webhook的签名密钥。

### 输出

-   **`image`**: 生成的图像，可连接到 `Preview Image` 等节点。
-   **`image_url`**: 生成图像的URL地址。
-   **`status`**: 显示生成状态，成功或失败的详细信息。

## ❗ 常见问题

-   **节点变红并提示未找到API密钥**:
    请严格按照上方的 **API 密钥设置** 步骤操作，确保 `.env` 文件位置正确、内容格式无误，并重启ComfyUI。
-   **生成失败/返回错误**:
    请检查 `status` 输出的错误信息。常见原因包括：账户余额不足、提示词触发安全策略、网络问题等。
-   **图生图效果不佳**:
    尝试调整 `guidance_scale` 参数。较低的值会给予输入图像更多权重，较高的值会更偏向于文本提示。

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🛠️ 开发信息

### 项目结构
```
ComfyUI-TuZi-Flux-Kontext/
├── __init__.py          # 节点注册入口
├── nodes.py             # 节点实现
├── api_client.py        # API客户端
├── utils.py             # 工具函数
├── config.py            # 配置管理
├── requirements.txt     # 依赖列表
└── README.md           # 说明文档
```

### 依赖项
- `requests>=2.25.0` - HTTP请求
- `pillow>=8.0.0` - 图像处理
- `numpy>=1.19.0` - 数值计算
- `torch>=1.9.0` - PyTorch
- `torchvision>=0.10.0` - 图像处理工具

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

- 📧 邮箱：support@example.com
- 💬 QQ群：123456789
- 🌐 官网：[tu-zi.com](https://tu-zi.com)

## 🔄 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎨 支持基础图像生成功能
- 🔧 支持高级参数配置
- 📱 完善的错误处理机制

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！** 