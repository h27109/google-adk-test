from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
import os

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