import uuid
import chromadb
from typing import List, Optional, Any
from langchain_openai import OpenAIEmbeddings

from src.core.memory import BaseMemory
from src.core.schemas import MemoryItem
from src.config.settings import settings

class ChromaMemory(BaseMemory):
    def __init__(self):
        # 1. 初始化 Chroma 客户端 (持久化到本地)
        self.client = chromadb.PersistentClient(
            path=settings.vector_store.chroma_persist_dir
        )
        
        # 2. 初始化嵌入模型 (用于把文本变成向量)
        # 注意：这里默认用 OpenAI 的 embedding，如果你想完全脱离 OpenAI，也可以换成 HuggingFace
        self.embedding_fn = OpenAIEmbeddings(
            openai_api_key=settings.llm.openai_api_key
        )
        
        # 3. 获取或创建集合
        self.collection = self.client.get_or_create_collection(
            name="agent_memory",
            metadata={"hnsw:space": "cosine"} # 使用余弦相似度
        )

    def add(self, item: MemoryItem) -> None:
        """添加单条记忆"""
        # 生成向量
        vector = self.embedding_fn.embed_query(item.content)
        
        # 存入 Chroma
        self.collection.add(
            ids=[str(uuid.uuid4())],
            embeddings=[vector],
            documents=[item.content],
            metadatas=[item.metadata]
        )

    def add_batch(self, items: List[MemoryItem]) -> None:
        """批量添加"""
        if not items:
            return
            
        vectors = self.embedding_fn.embed_documents([i.content for i in items])
        ids = [str(uuid.uuid4()) for _ in items]
        docs = [i.content for i in items]
        metas = [i.metadata for i in items]
        
        self.collection.add(
            ids=ids,
            embeddings=vectors,
            documents=docs,
            metadatas=metas
        )

    def search(self, query: str, limit: int = 3, filters: Optional[dict] = None) -> List[MemoryItem]:
        """检索记忆"""
        # 1. 把查询词变成向量
        query_vector = self.embedding_fn.embed_query(query)
        
        # 2. 在向量库中搜索
        results = self.collection.query(
            query_embeddings=[query_vector],
            n_results=limit,
            where=filters # Chroma 的 metadata 过滤语法
        )
        
        # 3. 转换回 MemoryItem 对象
        memory_items = []
        if results["documents"]:
            # Chroma 返回的是列表的列表，需要解包
            docs = results["documents"][0]
            metas = results["metadatas"][0]
            
            for doc, meta in zip(docs, metas):
                memory_items.append(MemoryItem(
                    content=doc,
                    metadata=meta
                ))
                
        return memory_items

    def clear(self) -> None:
        self.client.delete_collection("agent_memory")