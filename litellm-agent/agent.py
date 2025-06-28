"""
SiliconFlow金融分析智能体
基于Google ADK和LiteLLM的金融数据分析专家
"""

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
import os
import logging
from typing import Optional

from .tools import finance_toolsets, get_current_time

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv(override=True)


def setup_environment():
    """设置环境变量和API配置"""
    try:
        # 配置SiliconFlow API
        siliconflow_api_key = os.getenv("SILICONFLOW_API_KEY")
        siliconflow_model = os.getenv("SILICONFLOW_MODEL", "qwen-2.5-7b-instruct")
        
        if not siliconflow_api_key:
            raise ValueError("SILICONFLOW_API_KEY环境变量未设置")
        
        os.environ["OPENAI_API_KEY"] = siliconflow_api_key
        os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn"
        
        logger.info(f"使用模型: {siliconflow_model}")
        return siliconflow_model
        
    except Exception as e:
        logger.error(f"环境配置失败: {e}")
        raise


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
        model_name = setup_environment()
        
        agent = LlmAgent(
            model=LiteLlm(model=f"openai/{model_name}"),
            name="金融分析专家",
            instruction=create_agent_instruction(),
            description="专业的金融和投资分析专家，擅长股票、基金、债券等金融产品分析",
            tools=finance_toolsets,
            # 可以根据需要启用规划器
            # planner=PlanReActPlanner(),
        )
        
        logger.info("金融分析智能体创建成功")
        return agent
        
    except Exception as e:
        logger.error(f"智能体创建失败: {e}")
        raise


# 创建会话服务和运行器
def create_session_and_runner(agent: LlmAgent):
    """创建会话服务和运行器"""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=agent,
        app_name="金融分析应用",
        session_service=session_service
    )
    return session_service, runner


def call_agent_sync(query: str, session_service, runner, user_id: str = "user_001", session_id: str = "session_001"):
    """同步调用智能体"""
    try:
        # 确保会话存在
        try:
            session_service.get_session(app_name="金融分析应用", user_id=user_id, session_id=session_id)
        except:
            session_service.create_session(app_name="金融分析应用", user_id=user_id, session_id=session_id)
        
        # 创建用户消息
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        # 运行智能体
        events = runner.run(user_id=user_id, session_id=session_id, new_message=content)
        
        # 获取最终响应
        for event in events:
            if event.is_final_response():
                return event.content.parts[0].text
                
        return "未收到有效响应"
        
    except Exception as e:
        logger.error(f"智能体调用失败: {e}")
        return f"处理失败: {str(e)}"


# 主智能体实例
root_agent = create_finance_agent()

# 如果需要直接运行测试
if __name__ == "__main__":
    session_service, runner = create_session_and_runner(root_agent)
    
    # 测试查询
    test_query = "请帮我分析一下腾讯控股(00700.HK)的最新股价和基本面情况"
    response = call_agent_sync(test_query, session_service, runner)
    print(f"智能体回答: {response}")
