# app/chains.py
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from app.prompts import get_prompt
from app.config import OPENAI_MODEL
from app.memory import search_memory, add_memory

llm = ChatOpenAI(model=OPENAI_MODEL, temperature=0.7) # 创作需要一点创造力，温度设为0.7

def detect_platform(text: str):
    """简单的意图识别，决定用哪个 Prompt"""
    if "推特" in text or "X" in text or "twitter" in text.lower():
        return "x"
    elif "视频" in text or "脚本" in text or "口播" in text:
        return "video"
    else:
        return "xhs" # 默认为小红书

def run_chain(user_input: str):
    # 1. 识别平台意图
    platform = detect_platform(user_input)
    
    # 2. 检索相关记忆（比如你以前写过的类似话题）
    memories = search_memory(user_input, platform)
    memory_text = "\n".join([f"- {m.page_content}" for m in memories])
    
    # 3. 构建 Prompt
    system_content = get_prompt(platform)
    
    messages = [
        SystemMessage(content=system_content),
        SystemMessage(content=f"【长期记忆/参考风格】:\n{memory_text}"),
        HumanMessage(content=user_input)
    ]
    
    # 4. 调用 LLM (修正语法)
    response = llm.invoke(messages)
    content = response.content
    
    # 5. 写入记忆（把这次的创作思路存下来）
    # 只存用户的输入和 AI 的核心输出，避免存入无意义的对话
    full_record = f"用户需求: {user_input}\n生成内容: {content}"
    add_memory(full_record, platform)
    
    return f"【模式: {platform}】\n{content}"