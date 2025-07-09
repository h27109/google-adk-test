"""
多智能体金融分析系统示例
基于Google ADK多智能体最佳实践
"""

from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

from dotenv import load_dotenv
import os
import logging
from typing import List, Dict, Any

from common.finance_tool import finance_toolsets
from common.time_tool import get_current_time
from common.search_tool import search_web
from common.agent_setup import setup_model

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============= 专业智能体定义 =============

def create_stock_analyst() -> LlmAgent:
    """创建股票分析专家"""
    return LlmAgent(
        model=setup_model(),
        name="股票分析专家",
        description="专门分析个股技术面、基本面和估值，提供买卖建议",
        instruction=f"""
你是专业的股票分析师，当前时间: {get_current_time()['report']}

专业职责：
1. 技术分析：K线图、均线、MACD、RSI等技术指标分析
2. 基本面分析：财务报表、盈利能力、成长性分析  
3. 估值分析：PE、PB、PEG等估值指标
4. 投资建议：明确的买入/卖出/持有建议

分析要求：
- 基于实时数据进行分析
- 提供具体的数据支撑
- 给出明确的投资建议和目标价
- 提示风险因素
""",
        tools=[finance_toolsets[0], search_web]  # 股票数据工具
    )


def create_fund_analyst() -> LlmAgent:
    """创建基金分析专家"""
    return LlmAgent(
        model=setup_model(),
        name="基金分析专家", 
        description="专门分析基金业绩、投资组合和基金经理，提供基金投资建议",
        instruction=f"""
你是专业的基金分析师，当前时间: {get_current_time()['report']}

专业职责：
1. 基金业绩分析：收益率、夏普比率、最大回撤分析
2. 投资组合分析：持仓结构、行业配置、集中度分析
3. 基金经理分析：历史业绩、投资风格、稳定性评估
4. 基金对比：同类基金横向比较

分析要求：
- 从风险收益角度评估基金
- 分析基金的投资策略和风格
- 给出明确的配置建议
- 考虑投资者风险偏好
""",
        tools=[finance_toolsets[2], search_web]  # 基金数据工具
    )


def create_risk_analyst() -> LlmAgent:
    """创建风险评估专家"""
    return LlmAgent(
        model=setup_model(),
        name="风险评估专家",
        description="专门进行投资风险评估、风险控制和资产配置建议",
        instruction=f"""
你是专业的风险评估师，当前时间: {get_current_time()['report']}

专业职责：
1. 风险评估：市场风险、信用风险、流动性风险分析
2. 风险控制：止损策略、仓位管理、分散投资建议
3. 资产配置：根据风险偏好制定配置方案
4. 市场监控：宏观经济风险、政策风险提示

分析要求：
- 量化风险指标（VaR、波动率等）
- 提供具体的风险控制建议
- 根据市场环境调整策略
- 强调风险提示和预警
""",
        tools=[finance_toolsets[1], search_web]  # 财务数据工具（用于风险计算）
    )


def create_market_analyst() -> LlmAgent:
    """创建市场分析专家"""
    return LlmAgent(
        model=setup_model(),
        name="市场分析专家",
        description="专门分析宏观经济、行业趋势和市场情绪",
        instruction=f"""
你是专业的市场分析师，当前时间: {get_current_time()['report']}

专业职责：
1. 宏观分析：经济指标、货币政策、财政政策影响
2. 行业分析：行业景气度、竞争格局、发展趋势
3. 市场情绪：投资者情绪、资金流向、热点板块
4. 市场展望：短期和中长期市场走势判断

分析要求：
- 结合宏观经济数据
- 分析政策对市场的影响  
- 识别投资机会和风险
- 提供市场择时建议
""",
        tools=list(finance_toolsets) + [search_web]  # 可以使用所有数据工具
    )


# ============= 多智能体系统构建 =============

def create_financial_analysis_team() -> LlmAgent:
    """创建金融分析团队 - 层次结构模式"""
    load_dotenv(override=True)
    # 创建专业分析师
    stock_analyst = create_stock_analyst()
    fund_analyst = create_fund_analyst() 
    risk_analyst = create_risk_analyst()
    market_analyst = create_market_analyst()
    
    # 创建团队负责人
    team_leader = LlmAgent(
        model=setup_model(),
        name="金融分析团队负责人",
        description="协调金融分析团队，综合各专家意见提供投资决策",
        instruction=f"""
你是金融分析团队的负责人，当前时间: {get_current_time()['report']}

团队组成：
- 股票分析专家：负责个股分析和投资建议
- 基金分析专家：负责基金分析和配置建议  
- 风险评估专家：负责风险控制和资产配置
- 市场分析专家：负责宏观和行业分析

工作流程：
1. 根据用户问题判断需要哪些专家参与
2. 将任务委托给合适的专家团队成员
3. 综合各专家的分析结果
4. 给出最终的投资建议和风险提示

委托规则：
- 股票相关问题 -> 委托给股票分析专家
- 基金相关问题 -> 委托给基金分析专家  
- 风险评估问题 -> 委托给风险评估专家
- 市场趋势问题 -> 委托给市场分析专家
- 复杂问题可以委托给多个专家

最终输出要求：
- 综合所有专家意见
- 提供明确的投资建议
- 强调风险控制要点
- 给出具体的操作建议
""",
        sub_agents=[stock_analyst, fund_analyst, risk_analyst, market_analyst],
        tools=[search_web]  # 团队负责人可以使用所有工具
    )
    
    return team_leader


def create_workflow_analysis_system() -> SequentialAgent:
    """创建工作流分析系统 - 顺序执行模式"""
    load_dotenv(override=True)
    # 市场环境分析
    market_scanner = LlmAgent(
        model=setup_model(),
        name="市场环境扫描",
        description="扫描当前市场环境和宏观因素",
        instruction="分析当前市场环境、宏观经济状况和政策环境，为后续分析提供背景",
        tools=[finance_toolsets[1], search_web]  # 财务数据
    )
    
    # 投资机会识别
    opportunity_finder = LlmAgent(
        model=setup_model(),
        name="投资机会识别",
        description="基于市场环境识别投资机会",
        instruction="基于市场环境分析结果，识别当前的投资机会和热点板块",
        tools=[finance_toolsets[0], search_web]  # 股票数据
    )
    
    # 风险评估
    risk_evaluator = LlmAgent(
        model=setup_model(),
        name="风险评估",
        description="评估投资机会的风险水平",
        instruction="对识别出的投资机会进行风险评估，提供风险控制建议",
        tools=[finance_toolsets[1], search_web]  # 财务数据用于风险计算
    )
    
    # 投资建议整合
    recommendation_integrator = LlmAgent(
        model=setup_model(),
        name="投资建议整合",
        description="整合分析结果，提供最终投资建议",
        instruction="整合前面的分析结果，提供综合的投资建议和操作策略",
        tools=list(finance_toolsets) + [search_web]  # 可以使用所有工具进行验证
    )
    
    return SequentialAgent(
        name="投资分析工作流",
        sub_agents=[market_scanner, opportunity_finder, risk_evaluator, recommendation_integrator]
    )


def create_parallel_analysis_system() -> ParallelAgent:
    """创建并行分析系统 - 并行执行模式"""
    load_dotenv(override=True)
    return ParallelAgent(
        name="并行投资分析",
        sub_agents=[
            create_stock_analyst(),
            create_fund_analyst(),
            create_risk_analyst(),
            create_market_analyst()
        ]
    )

root_agent = create_financial_analysis_team()