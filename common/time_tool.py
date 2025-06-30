import datetime
from zoneinfo import ZoneInfo
from typing import Dict, Any
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