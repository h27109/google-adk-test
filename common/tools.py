"""
金融分析工具集
包含股票、基金、财务数据的MCP工具集配置
"""

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any, List
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


def get_current_time() -> Dict[str, Any]:
    """获取当前时间（上海时区）

    Returns:
        dict: 包含状态和时间报告的字典
    """
    try:
        tz_identifier = "Asia/Shanghai"
        tz = ZoneInfo(tz_identifier)
        now = datetime.datetime.now(tz)
        report = f'当前时间是 {now.strftime("%Y年%m月%d日 %H:%M:%S")} (上海时间)'
        return {"status": "success", "report": report}
    except Exception as e:
        return {"status": "error", "report": f"获取时间失败: {str(e)}"}


# 创建Tushare金融数据MCP工具集
def create_finance_toolsets() -> List[MCPToolset]:
    """创建金融数据相关的MCP工具集
    
    Returns:
        list: 包含股票、财务、基金数据的MCP工具集列表
    """
    
    # 获取认证信息
    api_key = os.getenv("TUSHARE_MCP_KEY")
    if not api_key:
        raise ValueError("TUSHARE_MCP_KEY环境变量未设置，请在.env文件中配置")
    
    # 确保api_key格式正确（应该包含Bearer前缀）
    if not api_key.startswith("Bearer "):
        api_key = f"Bearer {api_key}"
    
    print("使用的API密钥:", api_key)
    
    # 股票数据工具集
    tushare_stock_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/stock/mcp/",
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        ),
    )
    
    # 财务数据工具集  
    tushare_finance_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/finance/mcp/",
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        ),
    )
    
    # 基金数据工具集
    tushare_fund_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/fund/mcp/",
            headers={
                "Authorization": api_key,
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            }
        ),
    )
    
    return [tushare_stock_mcp, tushare_finance_mcp, tushare_fund_mcp]


# 导出所有工具
finance_toolsets = create_finance_toolsets() 