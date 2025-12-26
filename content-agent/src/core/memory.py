from abc import ABC, abstractmethod
from typing import List, Optional, Any
from src.core.schemas import MemoryItem

class BaseMemory(ABC):
    """
    记忆模块抽象基类 (Interface)
    """
    
    @abstractmethod
    def add(self, item: MemoryItem) -> None:
        """写入单条记忆"""
        pass

    @abstractmethod
    def add_batch(self, items: List[MemoryItem]) -> None:
        """批量写入（提高效率）"""
        pass

    @abstractmethod
    def search(self, query: str, limit: int = 3, filters: Optional[dict] = None) -> List[MemoryItem]:
        """
        语义检索
        :param query: 用户的问题
        :param limit: 返回几条
        :param filters: 比如 {"platform": "xhs"} 只搜小红书相关的记忆
        """
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """清空库（慎用）"""
        pass