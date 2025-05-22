import os
from dotenv import load_dotenv

class Config:
    load_dotenv()
    DEEPSEEK_API_KEY = os.environ.get('DEEPSEEK_API_KEY')
    if not DEEPSEEK_API_KEY:
        raise ValueError("未找到 DEEPSEEK_API_KEY 环境变量")
    DEEPSEEK_MODEL = "deepseek-ai/DeepSeek-V3"
    SEARCH_MAX_RESULTS=1
    
    
        