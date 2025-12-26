import os
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# 定义项目根目录，方便定位 data 文件夹
ROOT_DIR = Path(__file__).parent.parent.parent

class Environment(str, Enum):
    LOCAL = "local"
    DEV = "dev"
    PROD = "prod"

class LLMProvider(str, Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"

class LLMSettings(BaseSettings):
    """LLM 相关配置"""
    provider: LLMProvider = Field(default=LLMProvider.OPENAI, alias="LLM_PROVIDER")
    
    # OpenAI 配置
    openai_api_key: Optional[str] = Field(None, alias="OPENAI_API_KEY")
    openai_model: str = Field("gpt-4o-mini", alias="OPENAI_MODEL")
    
    # DeepSeek 配置 (兼容 OpenAI SDK)
    deepseek_api_key: Optional[str] = Field(None, alias="DEEPSEEK_API_KEY")
    deepseek_base_url: str = Field("https://api.deepseek.com", alias="DEEPSEEK_BASE_URL")
    deepseek_model: str = Field("deepseek-chat", alias="DEEPSEEK_MODEL")

    temperature: float = 0.7

class VectorStoreSettings(BaseSettings):
    """向量数据库配置"""
    provider: str = Field("chroma", alias="VECTOR_STORE_PROVIDER") # chroma 或 qdrant
    
    # Chroma 配置
    chroma_persist_dir: str = Field(str(ROOT_DIR / "data" / "vector_store"), alias="CHROMA_DB_DIR")
    
    # Qdrant 配置 (预留)
    qdrant_url: Optional[str] = Field(None, alias="QDRANT_URL")
    qdrant_api_key: Optional[str] = Field(None, alias="QDRANT_API_KEY")

class AppSettings(BaseSettings):
    """主应用配置"""
    env: Environment = Field(Environment.LOCAL, alias="APP_ENV")
    debug: bool = False
    
    # 嵌套子配置
    llm: LLMSettings = Field(default_factory=LLMSettings)
    vector_store: VectorStoreSettings = Field(default_factory=VectorStoreSettings)

    # 允许从 .env 文件读取
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        extra="ignore" # 忽略 .env 里多余的字段
    )

# 单例模式：整个项目只用这一个 settings 对象
settings = AppSettings()

# 打印一下加载路径，确保没搞错（调试用）
if settings.debug:
    print(f"Loaded config for env: {settings.env}")
    print(f"Project Root: {ROOT_DIR}")