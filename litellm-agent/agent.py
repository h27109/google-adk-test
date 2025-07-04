"""
SiliconFlow金融分析智能体
基于Google ADK和LiteLLM的金融数据分析专家
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from dotenv import load_dotenv
import os
import logging

from common.finance_tool import finance_toolsets
from common.time_tool import get_current_time
from common.search_tool import search_web

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv(override=True)



def setup_siliconflow_model():
    """配置SiliconFlow模型"""
    api_key = os.getenv("SILICONFLOW_API_KEY")
    if api_key is None:
        raise ValueError("SILICONFLOW_API_KEY 环境变量未设置")
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn"
    model_name = os.getenv("SILICONFLOW_MODEL", "Pro/deepseek-ai/DeepSeek-V3")
    return LiteLlm(model=f"openai/{model_name}")

def setup_deepseek_model():
    """配置DeepSeek模型"""
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if api_key is None:
        raise ValueError("DEEPSEEK_API_KEY 环境变量未设置")
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"
    model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    return LiteLlm(model=f"openai/{model_name}")

def setup_tencent_model():
    """配置腾讯模型"""
    api_key = os.getenv("TENCENT_API_KEY")
    if api_key is None:
        raise ValueError("TENCENT_API_KEY 环境变量未设置")
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = os.getenv("TENCENT_BASE_URL","https://api.hunyuan.cloud.tencent.com/v1")
    model_name = os.getenv("TENCENT_MODEL", "hunyuan-t1-latest")
    return LiteLlm(model=f"openai/{model_name}")

def setup_model():
    model_provider = os.getenv("MODEL_PROVIDER").lower()
    if model_provider == "siliconflow":
        return setup_siliconflow_model()
    elif model_provider == "deepseek":
        return setup_deepseek_model()
    elif model_provider == "tencent":
        return setup_tencent_model()
    else:
        raise ValueError(f"不支持的模型提供者: {model_provider}")


def create_agent_instruction() -> str:
    """创建智能体指令，包含当前时间信息"""
    current_time = get_current_time()
    
    instruction = f"""
你是一个专业的金融和投资分析专家，专门帮助用户分析股票、基金、债券等金融产品。

重要信息：
- {current_time['report']}
- 始终使用中文回答
- 提供专业、准确的金融建议
- 在分析时考虑风险因素
- 基于实时数据进行分析

你的专业领域包括：
1. 股票分析：技术分析、基本面分析、估值分析
2. 基金分析：基金业绩、投资组合、风险评估
3. 财务分析：财务报表分析、盈利能力、偿债能力
4. 投资建议：资产配置、风险管理、投资策略

在回答时请：
- 结合最新的市场数据
- 提供清晰的分析逻辑
- 给出具体的数据支撑
- 考虑风险提示
"""
    return instruction.strip()


# 创建智能体
def create_finance_agent() -> LlmAgent:
    """创建金融分析智能体"""
    try:
        
        model = setup_model()
        agent = LlmAgent(
            model=model,
            name="金融分析专家",
            instruction=create_agent_instruction(),
            description="专业的金融和投资分析专家，擅长股票、基金、债券等金融产品分析",
            tools=list(finance_toolsets) + [search_web],
            #tools=[search_web],
            # 可以根据需要启用规划器
            # planner=PlanReActPlanner(),
        )
        logger.info("金融分析智能体创建成功")
        return agent
        
    except Exception as e:
        logger.error(f"智能体创建失败: {e}")
        raise

# 主智能体实例
root_agent = create_finance_agent()
