# ComfyUI-TuZi-Flux-Kontext

�� **Flux-Kontext Pro/Max** 的 ComfyUI 自定义节点，使用兔子AI官方API，支持文生图和图生图。

## ✨ 特性

- 🎨 **高质量图像生成** - 支持 Flux-Kontext-Pro 和 Flux-Kontext-Max 两个模型，提供文生图和图生图功能
- 🔥 **批量生成** - 支持同时生成 1、2、4 张图像，提高生成效率
- ⚙️ **丰富的参数控制** - 支持调整指导强度(Guidance)、推理步数(Steps)、宽高比、种子等核心参数
- 🔑 **专业的密钥管理** - 通过 `.env` 文件或环境变量配置API密钥，安全且方便
- 🛡️ **健壮的错误处理** - 在API密钥未配置时提供清晰的中文指引，并在节点执行失败时尽量维持工作流不中断
- ⚡ **并发生成** - 多图像生成时使用线程池并发执行，显著提升生成速度
- 🎯 **智能种子管理** - 支持固定种子、递增种子和随机种子等多种生成模式

## 📦 安装

### 方法一：Git 克隆 (推荐)

1. 打开您的ComfyUI安装目录
2. 进入 `custom_nodes` 文件夹
3. 克隆本项目：
   ```bash
   cd ComfyUI/custom_nodes/
   git clone https://github.com/your-username/ComfyUI-TuZi-Flux-Kontext.git
   ```
4. 安装依赖：
   ```bash
   cd ComfyUI-TuZi-Flux-Kontext
   pip install -r requirements.txt
   ```
5. 重启ComfyUI

### 方法二：手动下载

1. 下载本项目的ZIP文件并解压到 `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/`
2. 安装依赖：
   ```bash
   pip install torch torchvision requests numpy pillow python-dotenv
   ```
3. 重启ComfyUI

## 🔑 API 密钥设置

为了使用本节点，您需要配置您的兔子AI API密钥。我们推荐使用 `.env` 文件的方式。

1.  **获取密钥**: 访问 [兔子AI官网](https://tu-zi.com) 并登录，在控制台获取您的 API 密钥。

### 配置方法

**推荐方式：使用 .env 文件**

1. 在 `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/` 目录下创建 `.env` 文件
2. 添加以下内容：
   ```
   TUZI_API_KEY=your-api-key-here
   ```
3. 保存文件并重启ComfyUI

**或者设置环境变量：**
```bash
# Windows
set TUZI_API_KEY=your-api-key-here

# Linux/Mac
export TUZI_API_KEY=your-api-key-here
```

⚠️ **注意**：如果未正确配置密钥，节点将显示红色错误信息并提供详细的设置指引。

## 🚀 使用方法

### 添加节点

在ComfyUI中，添加 `🐰 Flux Kontext API` 节点，位于 `TuZi/Flux-Kontext` 分类下。

### 输入参数说明

#### 必需参数

- **`prompt`** (文本): 图像描述提示词，支持多行输入
- **`model`**: 选择模型
  - `flux-kontext-pro`: 标准版本，平衡质量与速度
  - `flux-kontext-max`: 增强版本，更高质量但生成时间更长
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

- **`image`**: 生成的图像张量，可连接到其他节点
- **`image_url`**: 生成图像的URL地址
- **`status`**: 生成状态信息，包括成功数量和错误详情

### 使用技巧

1. **文生图模式**：只填写 `prompt` 参数，不连接 `image` 输入
2. **图生图模式**：连接图像到 `image` 输入，调整 `guidance_scale` 控制原图影响程度
3. **批量生成**：选择 `num_images` 为 2 或 4，系统会并发生成提升速度
4. **种子控制**：
   - 种子为0：每次生成随机结果
   - 种子非0：每张图使用递增种子 (seed, seed+1, seed+2...)

## ❗ 常见问题

### 节点错误

**Q: 节点变红并提示"未找到API密钥"**
A: 请确保：
- `.env` 文件位于正确位置
- 文件内容格式正确 (`TUZI_API_KEY=your-key`)
- 重启了ComfyUI

**Q: 生成失败/返回错误**
A: 检查 `status` 输出的详细错误信息，常见原因：
- 账户余额不足
- 提示词触发安全策略 (调整 `safety_tolerance`)
- 网络连接问题
- API密钥无效

### 生成质量

**Q: 图生图效果不理想**
A: 尝试调整以下参数：
- `guidance_scale`: 较低值更偏向原图，较高值更偏向提示词
- `num_inference_steps`: 增加步数可能提升细节
- `prompt_upsampling`: 启用提示词增强

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
- `torch` - PyTorch深度学习框架
- `torchvision` - 图像处理工具
- `requests` - HTTP请求库
- `numpy` - 数值计算库
- `pillow` - 图像处理库
- `python-dotenv` - 环境变量管理

```

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