# ComfyUI-TuZi-Flux-Kontext

🐰 **强大的 Flux-Kontext 图像生成** ComfyUI 自定义节点，使用兔子AI官方API，支持文生图、图生图和多图生图。 Pro模型0.14元/次，Max模型0.28元/次。

---

## 🚀 概述

ComfyUI-TuZi-Flux-Kontext 是一个专业的 ComfyUI 扩展，提供完整的 Flux Kontext Pro/Max 图像生成功能。经过深度优化，为用户提供最简洁的配置体验和最强大的功能支持。

## 📸 功能演示

### 🎨 文生图模式

使用 **🐰Flux.1 Kontext - Text to Image** 节点，纯文本生成高质量图像：

![文生图演示](images/text-to-image-demo.png)

*生成效果：基于文字描述创建的老虎眼睛特写，细节丰富，质感逼真*

### 🖼️ 单图编辑模式

使用 **🐰Flux.1 Kontext - Editing** 节点，基于输入图像进行智能编辑：

![单图编辑演示](images/single-image-editing-demo.png)

*生成效果：基于提示词"坐在沙发上的角色和达尔马提亚犬"，同时生成4张不同变化的图像*

### 🎭 多图融合模式

使用 **🐰Flux.1 Kontext - Editing (Multi Image)** 节点，融合多个参考图像：

![多图融合演示](images/multi-image-editing-demo.png)

*复杂工作流：使用多个参考图像（人物+小狗）进行智能融合，创造出和谐统一的场景*

### ✨ 核心特性

- 🎨 **三种生成模式** - 文生图、单图编辑、多图编辑，满足所有创作需求
- 🔥 **双模型支持** - Flux-Kontext-Pro 和 Flux-Kontext-Max，质量与速度自由选择
- ⚡ **并发批量生成** - 支持同时生成 1、2、4 张图像，智能并发提升效率
- 🛡️ **零技术门槛** - 只需一个API密钥，自动处理所有技术细节
- 🎯 **专业参数控制** - 完整支持种子、指导强度、推理步数、宽高比等参数
- 🌟 **优雅的用户界面** - 简洁的状态反馈，清晰的生成进度提示

### 🔥 项目优势

- **🔑 超简化配置** - 仅需配置兔子AI密钥，无需额外的第三方服务配置
- **📱 友好的反馈** - 中文界面，emoji状态提示，清晰的成功/失败统计
- **🚀 高性能** - 智能并发生成，多图同时处理，大幅提升生成速度
- **🛡️ 稳定可靠** - 完善的错误处理，自动重试机制，确保生成成功率

---

## 📦 安装方法 (第一次重启安装完成后，关闭ComfyUI，填写 .env 文件中的api-key。再重启一遍 ComfyUI 即可运行)

### 方法一：通过 ComfyUI Manager 安装（推荐）

1. 在 ComfyUI 界面中打开 **ComfyUI Manager**
2. 点击 **"Install via Git URL"**
3. 输入：`https://github.com/LKbaba/ComfyUI-TuZi-Flux-Kontext.git`
4. 第一次重启安装完成后，关闭ComfyUI，填写 .env 文件中的api-key。再重启一遍 ComfyUI 即可运行。

### 方法二：手动安装

#### 方式A：通过 Git 克隆（推荐）

```bash
# 进入 ComfyUI 的 custom_nodes 目录
cd ComfyUI/custom_nodes/

# 克隆项目
git clone https://github.com/LKbaba/ComfyUI-TuZi-Flux-Kontext.git
cd ComfyUI-TuZi-Flux-Kontext

# 安装依赖
pip install -r requirements.txt
```

#### 方式B：下载 ZIP 文件

1. 访问 [项目页面](https://github.com/LKbaba/ComfyUI-TuZi-Flux-Kontext)
2. 点击绿色 **"Code"** 按钮 → **"Download ZIP"**
3. 解压到 `ComfyUI/custom_nodes/` 目录
4. **重要**: 将解压后的文件夹从 `ComfyUI-TuZi-Flux-Kontext-main` 重命名为 `ComfyUI-TuZi-Flux-Kontext`

```bash
# 安装依赖
cd ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext
pip install -r requirements.txt
```

### 便携版用户特别说明

便携版用户需要使用ComfyUI自带的Python环境安装依赖：

**Git 克隆方式：**

```powershell
# 在 ComfyUI 根目录执行 例如：PS E:\ComfyUI_windows_portable_nvidia\ComfyUI_windows_portable>
 .\python_embeded\python.exe -m pip install --force-reinstall -r .\ComfyUI\custom_nodes\ComfyUI-TuZi-Flux-Kontext\requirements.txt
```

**ZIP 下载方式：**

```powershell
# ⚠️ 注意：如果是下载ZIP解压，文件夹名称为 ComfyUI-TuZi-Flux-Kontext-main
# 请先重命名文件夹，或使用以下命令：
 .\python_embeded\python.exe -m pip install --force-reinstall -r .\ComfyUI\custom_nodes\ComfyUI-TuZi-Flux-Kontext-main\requirements.txt

# 重命名后推荐使用：
 .\python_embeded\python.exe -m pip install --force-reinstall -r .\ComfyUI\custom_nodes\ComfyUI-TuZi-Flux-Kontext\requirements.txt
```

---

## 🔑 API密钥设置

### 获取 API 密钥

您只需要获取 **一个** API 密钥：

- **兔子AI密钥**: 访问 [兔子AI官网](https://api.tu-zi.com/panel) 登录后在控制台获取

### 配置方法

插件已经包含了 `.env` 配置模板文件，您只需要：

1. **打开配置文件**: `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/.env`
2. **替换 API 密钥**: 将 `sk-xxxxx` 替换为您的真实密钥

```env
TUZI_API_KEY=your_tuzi_api_key_here
```

**配置位置**: `ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext/.env`

### 配置完成

保存文件后重启 ComfyUI 即可使用！

---

## 🎯 使用方法

安装完成后，您将在 **"TuZi/Flux.1 Kontext"** 分类下找到三个强大的节点：

### 1. 🐰Flux.1 Kontext - Text to Image

**纯文本生成图像**

- **输入**: 文本提示词
- **用途**: 基于文字描述创建全新图像
- **支持模型**: Flux-Kontext-Pro、Flux-Kontext-Max
- **输出**: 高质量图像

### 2. 🐰Flux.1 Kontext - Editing

**单图像编辑生成**

- **输入**: 文本提示词 + 单张参考图像
- **用途**: 基于现有图像进行智能编辑和变换
- **支持模型**: Flux-Kontext-Pro、Flux-Kontext-Max
- **特色**: 深度理解图像上下文，精准编辑

### 3. 🐰Flux.1 Kontext - Editing (Multi Image)

**多图像融合生成**

- **输入**: 文本提示词 + 多张参考图像（2-4张）
- **用途**: 融合多个图像元素，创造复杂场景
- **支持模型**: Flux-Kontext-Pro、Flux-Kontext-Max
- **特色**: 智能理解多图关系，创造性融合

---

## ⚙️ 参数说明

### 核心参数

- **prompt** (文本提示词): 描述您想要生成的图像
- **model**: 选择生成模型
  - `flux-kontext-pro`:
    2025年6月3日
    一个统一的模型，提供本地编辑、生成性修改和 FLUX.1 质量的文本到图像生成。处理文本和图像输入，以实现精确的区域编辑或全场景转换，速度突破，开创了在多次编辑中保持角色一致性的迭代工作流程。
  - `flux-kontext-max`:
    2025年6月3日
    我们的新高级模型在各个方面都带来了最大性能——显著改善的提示遵循和排版生成实现了高端的一致性，使编辑在速度上没有妥协。
- **num_images**: 生成数量 (1/2/4 张)
- **seed**: 随机种子 (0=随机，其他=固定)

### 高级参数

- **guidance_scale**: 指导强度 (0.0-10.0)
  - 值越高，越严格遵循提示词
- **num_inference_steps**: 推理步数 (1-100)
  - 步数越多，细节越丰富
- **aspect_ratio**: 宽高比选择
  - 支持 21:9、16:9、4:3、1:1、3:4、9:16、9:21
- **output_format**: 输出格式 (PNG/JPEG)
- **safety_tolerance**: 安全容忍度 (0-6)
- **prompt_upsampling**: 提示词增强 (开启/关闭)

---

## 📋 系统要求

- **Python** >= 3.8
- **ComfyUI** (最新版本)
- **依赖包**:
  - requests
  - python-dotenv
  - fal-client
  - httpx
  - httpcore

---

## 🐛 故障排除

### 节点相关问题

**节点没有出现？**

- 完全重启 ComfyUI
- 检查插件安装路径：`ComfyUI/custom_nodes/ComfyUI-TuZi-Flux-Kontext`
- 确认依赖安装成功：`pip list | grep fal-client`

**节点显示红色错误？**

- 检查 `.env` 文件是否存在
- 验证 API 密钥格式：`TUZI_API_KEY=your_key_here`
- 重启 ComfyUI

### API 相关问题

**生成失败？**

- 检查兔子AI账户余额
- 验证 API 密钥有效性
- 查看节点状态信息获取详细错误

### 图像编辑问题

**编辑效果不理想？**

- 选择 `flux-kontext-max` 模型
- 优化提示词描述
- 尝试不同的 `seed` 值

---

## 🔮 更新日志

### v1.0.0

- ✨ **全新发布** - 三种生成模式完整支持
- 🔑 **简化配置** - 仅需一个 API 密钥
- ⚡ **并发优化** - 智能多线程生成
- 🌟 **用户体验** - 中文界面，友好反馈
- 🛡️ **稳定性** - 完善错误处理和重试机制

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

## 🤝 贡献与支持

### 贡献代码

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建功能分支
3. 提交代码更改
4. 发起 Pull Request

### 获取支持

- **项目文档**: GitHub 仓库
- **问题反馈**: GitHub Issues
- **兔子AI官网**: [tu-zi.com](https://api.tu-zi.com)
- **API文档**: [wiki.tu-zi.com](https://wiki.tu-zi.com/zh/Code/Flux-Kontext)

---

## 🔗 相关链接

- **兔子AI官网**: [tu-zi.com](https://api.tu-zi.com)
- **ComfyUI**: [github.com/comfyanonymous/ComfyUI](https://github.com/comfyanonymous/ComfyUI)
- **Flux模型**: [Black Forest Labs](https://blackforestlabs.ai/)

---

**⭐ 如果这个项目对您有帮助，请给我们一个星标！您的支持是我们持续改进的动力！**
