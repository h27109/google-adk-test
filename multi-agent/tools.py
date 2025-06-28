"""
金融分析工具集
包含股票、基金、财务数据的MCP工具集配置
"""

from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StreamableHTTPConnectionParams
import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any


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
def create_finance_toolsets():
    """创建金融数据相关的MCP工具集
    
    Returns:
        list: 包含股票、财务、基金数据的MCP工具集列表
    """
    
    # 股票数据工具集
    tushare_stock_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/stock/mcp",
        ),
        name="股票数据工具",
    )
    
    # 财务数据工具集  
    tushare_finance_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/finance/mcp",
        ),
        name="财务数据工具",
    )
    
    # 基金数据工具集
    tushare_fund_mcp = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url="http://39.108.114.122:8000/fund/mcp",
        ),
        name="基金数据工具",
    )
    
    return [tushare_stock_mcp, tushare_finance_mcp, tushare_fund_mcp]


# 导出所有工具
finance_toolsets = create_finance_toolsets() 