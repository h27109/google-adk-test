from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
from google.adk.planners.plan_re_act_planner import PlanReActPlanner

from dotenv import load_dotenv
import os
import datetime
from zoneinfo import ZoneInfo

load_dotenv(override=True)

tushare_stock_mcp = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url = "http://39.108.114.122:8000/stock/mcp",
            ),
        )
tushare_finance_mcp = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url = "http://39.108.114.122:8000/finance/mcp",
            ),
        )
tushare_fund_mcp = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url = "http://39.108.114.122:8000/fund/mcp",
            ),
        )

def get_current_time() -> dict:
    """Returns the current time in a current timezone.

    Returns:
        dict: status and result or error msg.
    """

    tz_identifier = "Asia/Shanghai"
    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = (
        f'The current time in {tz_identifier} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    )
    return {"status": "success", "report": report}

os.environ["OPENAI_API_KEY"] = os.getenv("SILICONFLOW_API_KEY")
os.environ["OPENAI_BASE_URL"] = "https://api.siliconflow.cn"

current_time = get_current_time()
instruction = """
你是一个金融和财务及投资分析专家，可以帮助用户分析股票、基金、债券等金融产品。
注意：1.当前时间是 {current_time}
     2.始终使用中文回答
""".format(current_time=current_time['report'])

root_agent = LlmAgent(
    model = LiteLlm(model = "openai/" + os.getenv("SILICONFLOW_MODEL")),
    name = "siliconflow_agent",
    instruction = instruction,
    description = "你是一个金融和财务及投资分析专家，可以帮助用户分析股票、基金、债券等金融产品",
    planner = PlanReActPlanner(),
    tools = [tushare_stock_mcp, tushare_finance_mcp, tushare_fund_mcp]
)
