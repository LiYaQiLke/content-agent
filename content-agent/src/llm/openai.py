from typing import List, Dict, Optional
from openai import OpenAI
from src.core.llm import BaseLLM
from src.config.settings import settings

class OpenAILLM(BaseLLM):
    def __init__(self):
        # 依赖注入：从 settings 读取 Key
        self.client = OpenAI(api_key=settings.llm.openai_api_key)
        self.model = settings.llm.openai_model
        
    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        """
        调用 OpenAI Chat 接口
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.llm.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            # 实际生产中这里应该记录日志
            return f"Error calling OpenAI: {str(e)}"

    # 简单生成接口（可选实现）
    def generate(self, prompt: str) -> str:
        return self.chat([{"role": "user", "content": prompt}])