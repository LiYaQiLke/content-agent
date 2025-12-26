from abc import ABC, abstractmethod
from typing import List, Dict, Union, Optional

class BaseLLM(ABC):
    """
    LLM 统一接口
    """
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> str:
        """
        多轮对话接口
        messages = [{"role": "user", "content": "..."}]
        """
        pass