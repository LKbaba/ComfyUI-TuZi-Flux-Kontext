# ComfyUI-TuZi-Flux-Kontext

🐰 **Flux-Kontext Pro/Max** 的 ComfyUI 自定义节点，使用兔子AI官方API，支持文生图和图生图。

## ✨ 特性

- 🎨 **高质量图像生成** - 支持 Flux-Kontext-Pro 和 Flux-Kontext-Max 两个模型
- 🚀 **完整的图生图支持** - 通过 `fal.ai` 实现稳定高效的图片上传，真正释放图生图潜力
- 🔥 **批量生成** - 支持同时生成 1、2、4 张图像，提高生成效率
- ⚙️ **丰富的参数控制** - 支持调整指导强度(Guidance)、推理步数(Steps)、宽高比、种子等核心参数
- 🔑 **专业的双密钥管理** - 通过 `.env` 文件或环境变量分别配置生成API和上传API的密钥，安全且方便
- 🛡️ **健壮的错误处理** - 在API密钥未配置时提供清晰的中文指引，并在节点执行失败时尽量维持工作流不中断
- ⚡ **并发生成** - 多图像生成时使用线程池并发执行，显著提升生成速度

## 📦 安装

1.  **克隆或下载项目**
    *   **Git克隆 (推荐)**:
        ```bash
        # 进入 ComfyUI 的 custom_nodes 目录
        cd ComfyUI/custom_nodes/
        git clone https://github.com/your-username/ComfyUI-TuZi-Flux-Kontext.git
        cd ComfyUI-TuZi-Flux-Kontext
        ```
    *   **手动下载**: 下载ZIP包解压到 `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/` 目录。

2.  **安装依赖**
    *   **普通版用户**:
        ```bash
        # 确保你已经 cd 到插件目录
        pip install -r requirements.txt
        ```
    *   **便携版用户 (重要!)**:
        您需要使用ComfyUI自带的Python环境来安装依赖。请在 **ComfyUI的根目录** (例如 `ComfyUI_windows_portable`) 打开PowerShell或CMD，然后运行以下命令：
        ```powershell
        # PowerShell 示例 (请根据您的实际路径调整)
        .\python_embeded\python.exe -m pip install -r .\ComfyUI\custom_nodes\ComfyUI-TuZi-Flux-Kontext\requirements.txt
        ```

3.  **重启ComfyUI**

## 🔑 API 密钥设置

为了使用本节点，您需要配置两个API密钥。我们推荐使用 `.env` 文件的方式。

1.  **获取密钥**:
    *   **兔子AI密钥 (`TUZI_API_KEY`)**: 访问 [兔子AI官网](https://tu-zi.com) 并登录，在控制台获取您的API密钥。用于**图像生成**。
    *   **Fal.ai密钥 (`FAL_KEY`)**: 访问 [Fal.ai官网](https://fal.ai/) 注册并获取您的API密钥。用于**图生图时的图片上传**。

2.  **配置方法**
    在 `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/` 目录下创建 `.env` 文件，并添加以下内容 (替换为您的真实密钥):
    ```env
    TUZI_API_KEY=your-tuzi-api-key-here
    FAL_KEY=your-fal-api-key-here
    ```

3.  **保存文件并重启ComfyUI**

⚠️ **注意**：如果未正确配置密钥，节点将显示红色错误信息并提供详细的设置指引。

## 🚀 使用方法

### 添加节点

在ComfyUI中，添加 `🐰 Flux Kontext API` 节点，位于 `TuZi/Flux-Kontext` 分类下。

### 输入参数说明

#### 必需参数

- **`prompt`** (文本): 图像描述提示词
- **`model`**: 选择模型
  - `flux-kontext-pro`: 标准版本，平衡质量与速度 (仅支持文生图)
  - `flux-kontext-max`: 增强版本，更高质量 (支持文生图和图生图)
- **`num_images`**: 生成图像数量 (1/2/4张)
- **`seed`**: 随机种子 (0表示随机，非0表示固定种子)
- **`guidance_scale`**: 指导强度 (0.0-10.0，默认3.0)
  - 数值越高，生成图像与提示词关联性越强
- **`num_inference_steps`**: 推理步数 (1-100，默认28)
  - 步数越多，细节可能越丰富，但生成时间更长
- **`aspect_ratio`**: 图像宽高比
  - 支持从 21:9 到 9:21 的多种比例
- **`output_format`**: 输出格式 (jpeg/png)
- **`safety_tolerance`**: 内容安全容忍度 (0-6，默认2)
- **`prompt_upsampling`**: 是否启用提示词增强 (默认关闭)

#### 可选参数

- **`image`**: 输入图像 (连接后启用图生图模式)

### 输出结果

- **`image`**: 生成的图像张量
- **`image_url`**: 生成图像的URL地址
- **`status`**: 生成状态信息

### 使用技巧

1.  **文生图模式**：只填写 `prompt` 参数，不连接 `image` 输入。
2.  **图生图模式**：
    *   连接图像到 `image` 输入。
    *   **必须选择 `flux-kontext-max` 模型。**
    *   确保已在 `.env` 文件中正确配置 `FAL_KEY`。
3.  **批量生成**：选择 `num_images` 为 2 或 4，系统会并发生成提升速度。
4. **种子控制**：
   - 种子为0：每次生成随机结果
   - 种子非0：每张图使用递增种子 (seed, seed+1, seed+2...)

## ❗ 常见问题

### 节点错误

**Q: 节点变红并提示"未找到API密钥"**
A: 请确保：
- `.env` 文件位于正确位置 (`ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/`)。
- 文件内容格式正确 (`TUZI_API_KEY=your-key` 和 `FAL_KEY=your-key`)。
- 重启了ComfyUI。

**Q: 图生图失败并提示"未找到FAL_KEY"**
A: 这是专门为图生图设置的错误。请确保您已在`.env`文件中正确配置了`FAL_KEY`。

**Q: 生成失败/返回错误**
A: 检查 `status` 输出的详细错误信息，常见原因：
- 兔子AI账户余额不足。
- 提示词触发安全策略 (可尝试调整 `safety_tolerance`)。
- 网络连接问题。

### 生成质量

**Q: 图生图效果不理想**
A: 尝试调整以下参数：
- `guidance_scale`: 较低值更偏向原图，较高值更偏向提示词。
- `num_inference_steps`: 增加步数可能提升细节。

**Q: 生成速度慢**
A: 优化建议：
- 使用 `flux-kontext-pro` 而非 `flux-kontext-max`
- 减少 `num_inference_steps`
- 批量生成时充分利用并发能力

## 🛠️ 开发信息

### 项目结构
```
ComfyUI-TuZi-Flux-Kontext/
├── __init__.py          # 节点注册入口
├── nodes.py             # 节点实现 (支持并发生成)
├── api_client.py        # API客户端 (包含重试逻辑)
├── utils.py             # 工具函数 (图像处理等)
├── config.py            # 配置管理 (API密钥等)
├── requirements.txt     # 依赖列表
├── test_api.py          # 完整测试脚本
├── quick_test.py        # 快速测试脚本
└── README.md           # 说明文档
```

### 依赖项
- `requests`
- `python-dotenv`
- `fal-client`
- `httpx`
- `httpcore`

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发指南

1. Fork 本项目
2. 创建功能分支
3. 提交代码更改
4. 运行测试确保功能正常
5. 提交 Pull Request

## 📞 支持

- 🌐 官网：[tu-zi.com](https://tu-zi.com)
- 📖 API文档：[wiki.tu-zi.com](https://wiki.tu-zi.com/zh/Code/Flux-Kontext)

## 🔄 更新日志

### v1.0.0 (2024-01-XX)
- ✨ 初始版本发布
- 🎨 支持 Flux-Kontext-Pro 和 Flux-Kontext-Max 模型
- 🔥 支持批量生成 (1/2/4张)
- ⚡ 实现并发生成提升速度
- 🛡️ 完善的错误处理和重试机制
- 🔧 支持全参数控制
- 📱 智能种子管理
- 🔑 安全的API密钥配置

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！** 