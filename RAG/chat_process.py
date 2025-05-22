import logging.config
import requests
import logging
from config import Config

logging.basicConfig(
            filename='logs/chat.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

class ChatProcess:
    def __init__(self):
        self.config = Config()
        self.headers = {
            "Authorization": f"Bearer {self.config.DEEPSEEK_API_KEY}",  # 使用实例变量
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

    def generate_response(self, message, temperature=0.7, top_p=1.0):
        """调用DeepSeek API生成回答"""
        # 构造正确的消息格式
        messages = [
            {"role": "user", "content": message}
        ]
        
        payload = {
            "model": self.config.DEEPSEEK_MODEL,  # 使用实例变量
            "messages": messages,
            "temperature": temperature,
            "top_p": top_p
        }
        
        try:
            response = requests.post(
                "https://api.siliconflow.cn/v1/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            # 提取AI的回复
            return result['choices'][0]['message']['content']
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"API请求失败: {e.response.status_code}")
            return {"error": f"API请求失败: {e.response.status_code}"}
        except Exception as e:
            self.logger.error(f"API调用异常: {str(e)}")
            return {"error": "服务暂时不可用，请稍后重试"}


if __name__ == "__main__":
  
    
    # 确保日志目录存在
    
    
    # 初始化聊天处理器
    chatbot = ChatProcess()
    
    # 测试消息
    test_messages = [
        "你好",
        "今天天气如何？",
        "请推荐一本好书",
        "1+1等于多少？"
    ]
    
    # 依次发送测试消息并打印回复
    for message in test_messages:
        print(f"\n用户: {message}")
        response = chatbot.generate_response(message)
        
        # 打印回复（处理API错误情况）
        if isinstance(response, dict) and "error" in response:
            print(f"错误: {response['error']}")
        else:
            print(f"AI: {response}")