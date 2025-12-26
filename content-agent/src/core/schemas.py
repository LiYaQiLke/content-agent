from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class PlatformType(str, Enum):
    XHS = "xhs"
    TWITTER = "x"
    VIDEO = "video"
    LINKEDIN = "linkedin" # 预留扩展

class MemoryItem(BaseModel):
    """
    记忆单元：存入向量库的最小单位
    """
    content: str
    # metadata 用于存储平台、类型、时间，方便后续 RAG 过滤
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

class TaskPayload(BaseModel):
    """
    任务载荷：前端或命令行传来的原始需求
    """
    query: str
    platform: PlatformType = Field(default=PlatformType.XHS, description="目标平台")
    tone: Optional[str] = Field(None, description="强制指定的语气，如：犀利、温柔")
    
    # 允许额外的参数，比如 video_duration (视频时长)
    extra_params: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(use_enum_values=True)

class AgentResponse(BaseModel):
    """
    Agent 的最终交付物
    """
    content: str
    thought_process: Optional[str] = Field(None, description="AI的思考过程")
    suggested_tags: List[str] = Field(default_factory=list, description="推荐标签")
    
    # 预留：如果是视频，这里可以放分镜列表
    structured_data: Optional[Dict[str, Any]] = None