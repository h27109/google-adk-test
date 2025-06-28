"""
SiliconFlow金融分析智能体使用示例
演示如何按照Google ADK最佳实践使用智能体
"""

import asyncio
from agent import root_agent, create_session_and_runner, call_agent_sync
from tools import get_current_time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """主函数：演示智能体的基本使用"""
    try:
        logger.info("=== SiliconFlow金融分析智能体演示 ===")
        
        # 显示当前时间
        current_time = get_current_time()
        logger.info(f"当前时间: {current_time['report']}")
        
        # 创建会话服务和运行器
        session_service, runner = create_session_and_runner(root_agent)
        logger.info("会话服务和运行器创建成功")
        
        # 定义测试查询
        test_queries = [
            "请告诉我当前时间",
            "帮我分析一下贵州茅台(600519)的股价走势",
            "推荐几只优质的股票型基金",
            "分析一下最近的A股市场表现",
        ]
        
        # 执行测试查询
        for i, query in enumerate(test_queries, 1):
            logger.info(f"\n--- 测试查询 {i}: {query} ---")
            
            response = call_agent_sync(
                query=query,
                session_service=session_service,
                runner=runner,
                user_id="demo_user",
                session_id="demo_session"
            )
            
            print(f"用户问题: {query}")
            print(f"智能体回答: {response}")
            print("-" * 50)
        
        logger.info("演示完成!")
        
    except Exception as e:
        logger.error(f"演示过程中发生错误: {e}")
        raise


async def async_example():
    """异步使用示例（如果需要的话）"""
    logger.info("=== 异步使用示例 ===")
    
    # 这里可以添加异步调用的例子
    # 目前ADK的Runner主要支持同步调用
    logger.info("当前使用同步调用方式")


def interactive_mode():
    """交互式模式"""
    logger.info("=== 进入交互式模式 ===")
    logger.info("输入 'quit' 或 'exit' 退出")
    
    try:
        session_service, runner = create_session_and_runner(root_agent)
        
        while True:
            try:
                user_input = input("\n请输入您的问题: ").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出']:
                    logger.info("退出交互式模式")
                    break
                
                if not user_input:
                    continue
                
                response = call_agent_sync(
                    query=user_input,
                    session_service=session_service,
                    runner=runner,
                    user_id="interactive_user",
                    session_id="interactive_session"
                )
                
                print(f"\n智能体回答: {response}")
                
            except KeyboardInterrupt:
                logger.info("\n用户中断，退出交互式模式")
                break
            except Exception as e:
                logger.error(f"处理用户输入时发生错误: {e}")
                continue
                
    except Exception as e:
        logger.error(f"交互式模式初始化失败: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        # 交互式模式
        interactive_mode()
    else:
        # 演示模式
        main()
        
        # 如果需要异步示例
        # asyncio.run(async_example()) 