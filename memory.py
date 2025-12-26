# app/memory.py
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from app.config import OPENAI_API_KEY
import os

# 确保数据目录存在
os.makedirs("data/vector_store", exist_ok=True)

def get_vector_store():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # Chroma 0.5+ 会自动处理持久化，不需要手动 persist
    vector_store = Chroma(
        persist_directory="data/vector_store",
        embedding_function=embeddings,
        collection_name="media_agent_memory"
    )
    return vector_store

def add_memory(text: str, platform: str):
    """写入记忆，带上平台标签"""
    store = get_vector_store()
    store.add_texts(
        texts=[text], 
        metadatas=[{"platform": platform, "type": "history"}]
    )

def search_memory(query: str, platform: str, k=2):
    """
    检索记忆。
    注：MVP阶段我们先不做严格的 metadata 过滤（filter），
    而是让 LLM 看到所有相关的背景，因为有时灵感是通用的。
    """
    store = get_vector_store()
    results = store.similarity_search(query, k=k)
    return results