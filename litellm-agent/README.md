# SiliconFlow金融分析智能体

基于Google ADK和LiteLLM的专业金融数据分析智能体，采用ADK最佳实践重构。

## 🌟 主要特性

- **专业金融分析**: 支持股票、基金、债券等金融产品分析
- **实时数据**: 集成Tushare金融数据API
- **多模型支持**: 通过LiteLLM支持多种大语言模型
- **模块化设计**: 遵循ADK最佳实践，代码结构清晰
- **会话管理**: 完整的会话生命周期管理
- **错误处理**: 健壮的错误处理和日志记录

## 📁 项目结构

```
litellm-agent/
├── __init__.py         # 包初始化文件
├── agent.py           # 主智能体定义
├── tools.py           # 工具集配置
├── example.py         # 使用示例
└── README.md          # 说明文档
```

## 🚀 核心组件

### 1. 智能体 (agent.py)
- **LlmAgent**: 主智能体类，配置模型和指令
- **会话管理**: InMemorySessionService + Runner
- **环境配置**: 自动化的API密钥和环境设置

### 2. 工具集 (tools.py)
- **股票数据工具**: 实时股价、技术指标等
- **财务数据工具**: 财务报表、盈利分析等  
- **基金数据工具**: 基金净值、业绩排名等
- **时间工具**: 获取当前时间信息

### 3. 使用示例 (example.py)
- **演示模式**: 预设查询示例
- **交互模式**: 实时问答界面
- **异步支持**: 为未来扩展准备

## 🔧 环境配置

### 必需的环境变量

```bash
# SiliconFlow API配置
SILICONFLOW_API_KEY=your_api_key_here
SILICONFLOW_MODEL=qwen-2.5-7b-instruct  # 可选，默认值

# 其他配置
OPENAI_API_KEY=  # 自动设置，无需手动配置
OPENAI_BASE_URL= # 自动设置，无需手动配置
```

### 安装依赖

```bash
# 使用uv管理依赖
uv add google-adk
uv add litellm
uv add python-dotenv
```

## 💡 使用方法

### 1. 基本使用

```python
from litellm_agent.agent import root_agent, create_session_and_runner, call_agent_sync

# 创建会话和运行器
session_service, runner = create_session_and_runner(root_agent)

# 调用智能体
response = call_agent_sync(
    query="分析一下贵州茅台的投资价值",
    session_service=session_service,
    runner=runner
)
print(response)
```

### 2. ADK Web UI

```bash
# 启动ADK Web界面
adk web

# 访问 http://localhost:8000
# 选择 "金融分析专家" 智能体
```

### 3. 命令行演示

```bash
# 运行演示模式
python -m litellm_agent.example

# 交互式模式
python -m litellm_agent.example interactive
```

## 🔄 ADK最佳实践

本项目严格遵循Google ADK文档推荐的最佳实践：

### 1. **模块化设计**
- ✅ 工具分离到独立的`tools.py`
- ✅ 智能体配置在`agent.py`
- ✅ 使用示例在`example.py`

### 2. **会话管理**
- ✅ 使用`InMemorySessionService`
- ✅ 通过`Runner`管理智能体运行
- ✅ 支持多用户多会话

### 3. **错误处理**
- ✅ 完整的异常捕获和处理
- ✅ 结构化日志记录
- ✅ 优雅的降级策略

### 4. **配置管理**
- ✅ 环境变量自动化配置
- ✅ 模型参数可配置
- ✅ 工具集模块化

### 5. **类型安全**
- ✅ 使用类型提示
- ✅ 输入输出验证
- ✅ 返回值标准化

## 🎯 核心改进

相比原始代码，主要优化包括：

1. **代码结构**: 按功能模块分离，提高可维护性
2. **错误处理**: 增加完整的异常处理和日志
3. **会话管理**: 添加标准的ADK会话服务
4. **配置管理**: 自动化环境配置和验证
5. **文档化**: 完整的类型提示和文档字符串
6. **测试友好**: 提供完整的使用示例和测试用例

## 🤖 智能体能力

- **股票分析**: 技术分析、基本面分析、估值分析
- **基金分析**: 基金业绩、投资组合、风险评估  
- **财务分析**: 财务报表分析、盈利能力、偿债能力
- **投资建议**: 资产配置、风险管理、投资策略

## 🔍 技术栈

- **Google ADK**: 智能体开发框架
- **LiteLLM**: 多模型统一接口
- **SiliconFlow**: 大语言模型服务
- **Tushare**: 金融数据源
- **MCP**: 模型上下文协议

## �� 许可证

MIT License 