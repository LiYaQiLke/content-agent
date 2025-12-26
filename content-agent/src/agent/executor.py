import logging
from typing import Optional

from src.config.settings import settings, LLMProvider
from src.core.schemas import TaskPayload, AgentResponse, MemoryItem, PlatformType
from src.agent.prompts import get_system_prompt

# 引入具体实现类
# 注意：虽然这里引入了，但如果没 Key，只要不运行 run() 方法通常不会报错
from src.llm.openai import OpenAILLM
from src.llm.deepseek import DeepSeekLLM
from src.memory.chroma import ChromaMemory

logger = logging.getLogger(__name__)

class ContentExecutor:
    def __init__(self):
        # 1. 初始化记忆模块
        self.memory = ChromaMemory()
        
        # 2. 初始化 LLM (根据配置选择)
        if settings.llm.provider == LLMProvider.DEEPSEEK:
            self.llm = DeepSeekLLM()
        else:
            self.llm = OpenAILLM()
            
    def run(self, payload: TaskPayload) -> AgentResponse:
        """
        执行一次内容生成任务
        """
        logger.info(f"开始执行任务: {payload.query} | 平台: {payload.platform}")
        
        # --- Step 1: RAG 检索长期记忆 ---
        # 检索与当前 query 相关的历史风格或素材
        relevant_memories = self.memory.search(
            query=payload.query, 
            limit=3,
            filters={"platform": payload.platform} # 尽量参考同平台的过往内容
        )
        
        # 格式化记忆文本
        memory_context = "\n".join([f"- {m.content}" for m in relevant_memories])
        if not memory_context:
            memory_context = "暂无相关历史记忆。"
            
        # --- Step 2: 构建 Prompt ---
        system_prompt = get_system_prompt(payload.platform)
        
        # 如果用户指定了 tone (语气)，强制追加
        user_instruction = payload.query
        if payload.tone:
            user_instruction += f"\n\n【特别要求】请使用“{payload.tone}”的语气。"
            
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "system", "content": f"【参考的历史记忆/过往风格】:\n{memory_context}"},
            {"role": "user", "content": user_instruction}
        ]
        
        # --- Step 3: 调用 LLM ---
        # 这里暂时没做 try-catch，因为外层调用会处理，或者报错直接中断调试
        content = self.llm.chat(messages)
        
        # --- Step 4: 存入记忆 (闭环) ---
        # 只有当生成成功时才存入
        if content:
            # 存入用户的 Query (方便以后搜到类似需求)
            self.memory.add(MemoryItem(
                content=f"用户需求: {payload.query}",
                metadata={"type": "query", "platform": payload.platform}
            ))
            
            # 存入 AI 的回答 (方便以后模仿自己的文风)
            self.memory.add(MemoryItem(
                content=f"生成内容: {content}",
                metadata={"type": "response", "platform": payload.platform}
            ))
            
        return AgentResponse(
            content=content,
            thought_process="RAG retrieval -> Prompt construction -> LLM generation -> Memory update",
            suggested_tags=[] # 可以在 Prompt 里让 LLM 返回 JSON 来解析 tags，MVP 先留空
        )