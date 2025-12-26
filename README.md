# content-agent

内容代理（Content Agent） — Agent 驱动的内容生成系统 / Agent-based content generation system

版本：0.1.0

---

## 简介 (Overview)

这是一个基于 agent 架构的内容生成服务，目标是通过可组合的 agent、记忆层（向量数据库）和可配置的人设/提示来生成、管理并检索不同平台的内容（如文案、社媒帖子等）。

This is an agent-based content generation system. It composes agents, memory layers (vector stores), and configurable personas/prompts to generate, manage and retrieve content for different platforms (ads, social posts, copywriting, etc.).

## 特性 / Features

- 可组合的 agent 和链（chains）以实现复杂任务流
- 支持多种向量存储（Chroma、Qdrant）用于长期记忆与检索
- 基于 `pydantic` 的数据模型与类型安全
- 使用 `langchain` 集成 LLM 工作流
- 可通过 Docker 一键运行

- Composable agents and chains for complex workflows
- Support for multiple vector stores (Chroma, Qdrant) for persistent memory and retrieval
- Pydantic models for clear data schemas
- LangChain-based LLM workflows
- Docker-friendly for easy deployment

## 先决条件 / Requirements

- Python 3.10+
- 推荐使用虚拟环境（venv / pyenv）

依赖（摘自 `pyproject.toml`）:
- langchain>=0.2.0
- pydantic>=2.0
- python-dotenv
- loguru
- chromadb
- qdrant-client
- requests

The above dependencies are declared in `content-agent/pyproject.toml`.

## 快速开始 / Quick Start

1. 克隆并进入项目目录（示例以 `content-agent` 为示例子目录）:

```bash
cd content-agent
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt  # 如果你使用 requirements 文件
```

2. 配置环境变量：在项目根或 `content-agent` 下创建 `.env`，至少配置你的 LLM 相关密钥与向量库地址，例如：

```
OPENAI_API_KEY=sk-...
QDRANT_URL=http://localhost:6333
CHROMA_SETTINGS=... (可选)
```

3. 运行（以模块方式）:

```bash
python -m src.main
```

说明：项目入口位于 `content-agent/src/main.py`。根据你的环境，可能需要在运行前设置 `PYTHONPATH=src` 或通过 `pip install -e .` 将包可导入。

## Docker

项目包含 `Dockerfile` 与 `docker-compose.yml`（位于 `content-agent/docker/` 和根目录 `content-agent/docker-compose.yml`）。

构建并运行：

```bash
# 在 content-agent 目录下
docker-compose up --build
```

这将构建镜像并启动所需服务（例如向量数据库或代理服务，取决于 docker-compose 配置）。

## 项目结构 / Project Layout

- `src/` - 核心代码
	- `agent/` - agent 实现（chains、executor、prompts）
	- `core/` - 核心抽象（llm，memory，persona，task 等）
	- `llm/` - 各 LLM 提供者实现（OpenAI、DeepSeek 等）
	- `memory/` - 向量存储适配器（Chroma、Qdrant）
	- `utils/` - 环境与帮助函数
- `data/` - 持久化数据（personas、vector_store 等）
- `docker/` - Dockerfile 与 compose 配置
- `tests/` - 单元测试

（参见仓库根的文件结构以获取更详细内容）

## 配置与自定义 / Configuration & Customization

- Personas: 在 `data/personas/` 中定义或管理人物设定（可被 agent 加载用于生成风格化输出）。
- 向量存储：配置 Chroma 或 Qdrant 的连接信息，代码中已提供适配器（`src/memory/chroma.py`, `src/memory/qdrant.py`）。
- Prompts: 在 `src/agent/prompts.py` 中维护模板。

## 运行测试 / Tests

使用 pytest（`pyproject.toml` 已将 `src` 加入 pythonpath）：

```bash
cd content-agent
pytest
```

或指定测试文件：

```bash
pytest tests/test_agent.py
```

## 开发 / Development

- 建议先安装可编辑模式：

```bash
pip install -e .
```

- 代码风格 & 类型检查（建议）：

```bash
# 安装 linters（示例）
pip install black ruff mypy
black .
ruff .
mypy src
```

## 示例用例 / Example

仓库中包含一组演示与测试用例（见 `tests/`），用于展示 agent 如何执行任务。可根据 `src/agent` 中的接口扩展自定义 agent。

## FAQ / 常见问题

Q: 如何切换向量存储？
A: 修改配置并在运行前确保相应服务可用（比如启动 Qdrant 或使用本地 Chroma）。适配器代码位于 `src/memory/`。

Q: 没有 LLM 密钥怎么跑示例？
A: 可以用 mock 或本地 LLM（若已接入），或者将部分功能切换为不调用外部 API 的逻辑以运行离线测试。

## 许可证与贡献 / License & Contributing

本项目默认未指定许可证。若要发布请在仓库根添加 `LICENSE`。欢迎通过 PR 的方式贡献，提交前请运行测试并保持代码风格一致。



