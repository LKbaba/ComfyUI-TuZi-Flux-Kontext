# ComfyUI-TuZi-Flux-Kontext

🐰 **Flux-Kontext Pro** 的 ComfyUI 自定义节点，支持基于文本提示和参考图像生成高质量图像。

## ✨ 特性

- 🎨 **高质量图像生成** - 基于 Flux-Kontext-Pro 模型
- 🖼️ **多图参考支持** - 支持在提示词中包含图片URL
- ⚙️ **丰富的参数控制** - 宽高比、输出格式、安全容忍度等
- 🔧 **两种节点模式** - 基础版和高级版
- 🌐 **完善的错误处理** - 用户友好的错误提示
- 📱 **响应式设计** - 适配不同的使用场景

## 📦 安装

### 方法一：Git 克隆（推荐）

```bash
cd ComfyUI/custom_nodes/
git clone https://github.com/your-username/ComfyUI-TuZi-Flux-Kontext.git
cd ComfyUI-TuZi-Flux-Kontext
pip install -r requirements.txt
```

### 方法二：手动下载

1. 下载本项目的 ZIP 文件
2. 解压到 `ComfyUI/custom_nodes/` 目录
3. 安装依赖：`pip install -r requirements.txt`

## 🔑 API 密钥获取

1. 访问 [兔子AI官网](https://tu-zi.com)
2. 注册账号并登录
3. 在控制台获取 API 密钥（default分组）
4. 在节点中输入您的 API 密钥

### 环境变量配置（可选）

您也可以通过环境变量设置 API 密钥：

```bash
# Windows
set FLUX_KONTEXT_API_KEY=your-api-key-here

# Linux/Mac
export FLUX_KONTEXT_API_KEY=your-api-key-here
```

## 🚀 使用方法

### 基础节点：🐰 Flux-Kontext 图像生成

最简单的使用方式，包含核心功能：

**必填参数：**
- `prompt` - 图像描述提示词
- `api_key` - 您的 API 密钥

**可选参数：**
- `seed` - 随机种子（-1为随机）
- `aspect_ratio` - 宽高比选择
- `output_format` - 输出格式（jpeg/png）
- `safety_tolerance` - 安全容忍度（0-6）
- `prompt_upsampling` - 提示词增强

### 高级节点：🐰 Flux-Kontext 高级生成

支持更多高级功能：

**额外参数：**
- `webhook_url` - Webhook 通知 URL
- `webhook_secret` - Webhook 签名密钥
- `response_data` - 完整的 API 响应数据

### 提示词格式

#### 纯文本提示
```
一只可爱的橘猫坐在阳光下
```

#### 包含参考图像
```
https://example.com/image.jpg 让这个女人带上墨镜，衣服换个颜色
```

#### 多图参考
```
https://example.com/image1.jpg https://example.com/image2.jpg 请将P2中的女孩替换为P1中的女孩
```

## 📋 支持的参数

### 宽高比选项
- `1:1` - 正方形
- `16:9` - 宽屏
- `9:16` - 手机竖屏
- `4:3` - 标准屏幕
- `3:4` - 竖屏
- `21:9` - 超宽屏
- `9:21` - 超长竖屏

### 输出格式
- `jpeg` - JPEG 格式（默认）
- `png` - PNG 格式

### 安全容忍度
- `0-2` - 严格模式，适合商业用途
- `3-4` - 平衡模式，适合一般用途
- `5-6` - 宽松模式，创意内容

## 🔧 工作流示例

### 基础工作流
1. 添加 `🐰 Flux-Kontext 图像生成` 节点
2. 输入提示词和 API 密钥
3. 调整参数（可选）
4. 连接到 `Preview Image` 节点查看结果

### 高级工作流
1. 使用 `🐰 Flux-Kontext 高级生成` 节点
2. 配置 Webhook 参数（如需要）
3. 连接 `response_data` 输出到文本显示节点查看详细信息

## ❗ 常见问题

### Q: 提示 "API密钥无效或已过期"
A: 请检查：
- API 密钥是否正确输入
- 账户余额是否充足
- 网络连接是否正常

### Q: 图像下载失败
A: 可能原因：
- 网络连接问题
- 图像URL已过期
- 防火墙阻止了下载

### Q: 生成的图像是黑色的
A: 这通常表示出现了错误，请查看状态信息了解具体原因。

### Q: 如何使用多图参考？
A: 在提示词开头放置多个图片URL，用空格分隔：
```
https://image1.jpg https://image2.jpg 描述文字
```

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

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

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