# ComfyUI-TuZi-Flux-Kontext Project Structure

## Directory Structure

```
ComfyUI-TuZi-Flux-Kontext/
├── __init__.py                 # ComfyUI节点注册入口文件
├── nodes.py                    # 主要节点实现文件
├── api_client.py              # Flux-Kontext API客户端封装
├── utils.py                   # 工具函数集合
├── config.py                  # 配置管理模块
├── requirements.txt           # Python依赖包列表
├── README.md                  # 项目说明文档
├── TODO.md                    # 开发任务清单
├── structure.md               # 本文件，项目结构说明文档
├── examples/                  # 使用示例目录
│   ├── basic_workflow.json    # 基础工作流示例
│   ├── advanced_workflow.json # 高级工作流示例
│   └── screenshots/           # 节点使用截图
│       ├── node_interface.png
│       └── workflow_example.png
└── tests/                     # 测试文件目录（可选）
    ├── test_api_client.py
    ├── test_nodes.py
    └── test_utils.py
```

## File Details

### Core Files

#### `__init__.py`
- **作用**: ComfyUI自定义节点的注册入口
- **功能**:
  - 导入所有节点类
  - 定义 `NODE_CLASS_MAPPINGS` 字典
  - 定义 `NODE_DISPLAY_NAME_MAPPINGS` 字典
  - 设置节点分类和显示信息
- **重要性**: ★★★★★ (必须文件，ComfyUI识别节点的关键)

#### `nodes.py`
- **作用**: 主要的节点实现文件
- **功能**:
  - 定义 `FluxKontextNode` 主节点类
  - 实现节点的输入输出定义
  - 实现图像生成的核心逻辑
  - 处理ComfyUI与API之间的数据转换
- **重要性**: ★★★★★ (核心业务逻辑)

#### `api_client.py`
- **作用**: 封装Flux-Kontext API的调用逻辑
- **功能**:
  - 定义 `FluxKontextAPI` 类
  - 实现HTTP请求封装
  - 处理API认证和错误处理
  - 支持标准API和Chat API两种调用方式
- **重要性**: ★★★★★ (API交互核心)

### Supporting Files

#### `utils.py`
- **作用**: 提供通用工具函数
- **功能**:
  - 图像下载和格式转换
  - PIL图像与ComfyUI张量的相互转换
  - URL解析和验证
  - 数据格式化工具
- **重要性**: ★★★★☆ (重要辅助功能)

#### `config.py`
- **作用**: 配置管理模块
- **功能**:
  - API密钥管理
  - 默认参数配置
  - 环境变量读取
  - 配置验证和错误处理
- **重要性**: ★★★☆☆ (配置管理)

#### `requirements.txt`
- **作用**: Python依赖包管理
- **内容**:
  ```
  requests>=2.25.0
  pillow>=8.0.0
  numpy>=1.19.0
  torch>=1.9.0
  torchvision>=0.10.0
  ```
- **重要性**: ★★★★☆ (环境依赖)

### Documentation Files

#### `README.md`
- **作用**: 项目主要说明文档
- **内容**:
  - 项目介绍和特性
  - 安装和配置指南
  - 使用教程和示例
  - API密钥获取方法
  - 常见问题解答
- **重要性**: ★★★★☆ (用户体验关键)

#### `TODO.md`
- **作用**: 开发任务清单
- **内容**: 详细的开发计划和任务分解
- **重要性**: ★★★☆☆ (开发管理)

#### `structure.md`
- **作用**: 项目结构说明文档
- **内容**: 本文件，详细说明项目组织结构
- **重要性**: ★★★☆☆ (开发参考)

### Example Files

#### `examples/` 目录
- **作用**: 提供使用示例和演示
- **内容**:
  - `basic_workflow.json` - 基础使用工作流
  - `advanced_workflow.json` - 高级功能工作流
  - `screenshots/` - 界面截图和使用演示
- **重要性**: ★★★☆☆ (用户指导)

### Test Files (Optional)

#### `tests/` 目录
- **作用**: 单元测试和集成测试
- **内容**:
  - API客户端测试
  - 节点功能测试
  - 工具函数测试
- **重要性**: ★★☆☆☆ (质量保证)

## 开发顺序建议

### 第一阶段：核心框架
1. 创建基本文件结构
2. 实现 `api_client.py` 基础功能
3. 创建简单的 `nodes.py` 框架
4. 配置 `__init__.py` 注册机制

### 第二阶段：功能实现
1. 完善API客户端的所有功能
2. 实现节点的完整输入输出逻辑
3. 添加图像处理和转换功能
4. 实现错误处理机制

### 第三阶段：优化完善
1. 添加工具函数和配置管理
2. 完善错误处理和用户体验
3. 编写文档和使用示例
4. 进行测试和调试

## 技术架构

```
用户界面 (ComfyUI)
       ↓
节点层 (nodes.py)
       ↓
API客户端层 (api_client.py)
       ↓
网络层 (HTTP请求)
       ↓
Flux-Kontext API服务
```

## 数据流向

```
用户输入参数 → 节点处理 → API调用 → 图像生成 → 图像下载 → 格式转换 → ComfyUI显示
```

## 关键设计原则

1. **模块化设计**: 每个文件职责单一，便于维护
2. **错误处理**: 完善的异常处理和用户友好的错误信息
3. **可扩展性**: 预留接口，便于未来功能扩展
4. **标准兼容**: 严格遵循ComfyUI自定义节点开发规范
5. **用户体验**: 简单易用的界面和清晰的文档说明 