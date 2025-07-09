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
from common.agent_setup import setup_model

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
