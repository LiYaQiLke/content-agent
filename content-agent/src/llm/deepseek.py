from typing import List, Dict, Optional
from openai import OpenAI
from src.core.llm import BaseLLM
from src.config.settings import settings

class DeepSeekLLM(BaseLLM):
    def __init__(self):
        # DeepSeek 使用 OpenAI 的 SDK，但指向不同的 Base URL
        self.client = OpenAI(
            api_key=settings.llm.deepseek_api_key,
            base_url=settings.llm.deepseek_base_url
        )
        self.model = settings.llm.deepseek_model

    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or settings.llm.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling DeepSeek: {str(e)}"