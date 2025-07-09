# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import uuid
from typing import Dict, List, Optional, Tuple
import sys
import io
from common.time_tool import get_current_time
from common.agent_setup import setup_model

# 强制标准输出/错误流使用UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# --- 基本配置 ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv(override=True)

# --- 会话管理 ---
class PromptOptimizationSession:
    def __init__(self, session_id: str, user_id: str):
        self.session_id = session_id
        self.user_id = user_id
        self.history: List[Dict[str, str]] = []

    def add_turn(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def get_formatted_history(self) -> str:
        full_history_text = ""
        for turn in self.history:
            full_history_text += f"{turn['role']}: {turn['content']}\n"
        return full_history_text


# --- 核心智能体 ---
class PromptEngineerAgent:
    def __init__(self):
        self.model = setup_model()
        self.sessions: Dict[str, PromptOptimizationSession] = {}
        self.session_service = InMemorySessionService()
        self.agent = self._create_root_agent()

    def _create_root_agent(self) -> LlmAgent:
        instruction = f"""
                        你是一个专业的金融提示词优化专家。你的任务是帮助用户将他们模糊的金融想法，
                        转化为一个清晰、具体、可直接用于其他金融分析AI的专业提示词。
                        请根据用户的需求，以帮助用户完善最终的金融分析提示词。
                        注意当前时间是: {get_current_time()['report']} 
                        注意每轮对话只提一个问题
                        """
        return LlmAgent(
            model=self.model,
            name="金融提示词优化专家",
            description="通过多轮对话，将您模糊的金融问题，优化成精准、可执行的专业提示词。",
            instruction=instruction,
        )

    async def process(
        self,
        user_input: str,
        session_id: Optional[str] = None,
        user_id: str = "default_user",
    ) -> Tuple[str, Optional[str]]:
        if session_id and session_id in self.sessions:
            session = self.sessions[session_id]
        else:
            adk_session = await self.session_service.create_session(
                app_name="prompt_engineer", user_id=user_id
            )
            new_session_id = adk_session.id
            session = PromptOptimizationSession(new_session_id, user_id)
            self.sessions[new_session_id] = session

        # 将所有用户输入合并为一个完整的请求
        full_user_request = session.get_formatted_history() + f"用户: {user_input}"

        try:
            runner = Runner(
                agent=self.agent,
                app_name="prompt_engineer",
                session_service=self.session_service,
            )
            events = runner.run(
                user_id=session.user_id,
                session_id=session.session_id,
                new_message=types.Content(role="user", parts=[types.Part(text=full_user_request)]),
            )
            llm_response = ""
            for event in events:
                if event.is_final_response():
                    llm_response = event.content.parts[0].text
                    break
        except Exception as e:
            logger.error(f"LLM API call failed: {e}")
            return ("抱歉，AI服务暂时不可用，请稍后再试。", session.session_id)

        if not llm_response:
            return ("抱歉，我从AI收到了一个空响应，请再试一次。", session.session_id)

        session.add_turn("user", user_input)
        session.add_turn("assistant", llm_response)

        return llm_response, session.session_id

    @property
    def root_agent(self) -> LlmAgent:
        """返回根代理，供ADK Web UI使用"""
        return self.agent


# --- 测试用的主函数 ---
async def main():
    prompt_engineer = PromptEngineerAgent()

    print("--- 开始模拟多轮对话优化 ---")

    # 轮次 1: 用户初次查询
    print("\n--- Turn 1: Initial Query ---")
    user_query_1 = "我想投资股票"
    print(f"User > {user_query_1}")
    response_1, session_id = await prompt_engineer.process(user_query_1)
    print(f"Agent >\n{response_1}")

    # 轮次 2: 用户回答第一轮问题
    print("\n--- Turn 2: User's First Answer ---")
    user_query_2 = "我关注科技股，特别是AI领域的。打算长期投资，风险偏好比较高。"
    print(f"User > {user_query_2}")
    response_2, session_id = await prompt_engineer.process(user_query_2, session_id)
    print(f"Agent >\n{response_2}")

    # 轮次 3: 用户回答第二轮问题，并使用触发词
    print("\n--- Turn 3: User's Second Answer (Final Prompt) ---")
    user_query_3 = "我的投资金额大约在50万人民币。"
    print(f"User > {user_query_3}")
    response_3, session_id = await prompt_engineer.process(user_query_3, session_id)
    print(f"Agent >\n{response_3}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred: {e}")

# --- ADK Web UI的根Agent入口 ---
# 创建全局实例并导出根代理
_prompt_engineer_instance = PromptEngineerAgent()
root_agent = _prompt_engineer_instance.root_agent
