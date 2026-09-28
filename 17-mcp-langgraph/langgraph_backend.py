from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool, BaseTool
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_mcp_adapters.client import MultiServerMCPClient

from dotenv import load_dotenv

from typing import TypedDict, Annotated

import asyncio
import threading
import aiosqlite
import os
import requests


load_dotenv()


# Keep all async backend work on the same event loop.
_async_loop = asyncio.new_event_loop()

_async_thread = threading.Thread(
    target=_async_loop.run_forever,
    daemon=True,
)

_async_thread.start()


def run_async(coro):
    future = asyncio.run_coroutine_threadsafe(
        coro,
        _async_loop,
    )
    return future.result()


def submit_async(coro):
    return asyncio.run_coroutine_threadsafe(
        coro,
        _async_loop,
    )


llm = ChatOpenAI(
    model="openai/gpt-oss-20b",
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL"),
    max_tokens=300,
    temperature=0.5,
)


search_tool = DuckDuckGoSearchRun(region="us-en")


@tool
def get_stock_price(symbol: str) -> dict:
    """Get the latest stock price for a stock symbol."""

    api_key = os.getenv("STOCK_API_KEY")

    url = (
        "https://www.alphavantage.co/query"
        f"?function=GLOBAL_QUOTE"
        f"&symbol={symbol}"
        f"&apikey={api_key}"
    )

    response = requests.get(url)
    response.raise_for_status()

    return response.json()


client = MultiServerMCPClient(
    {
        "arith": {
            "transport": "stdio",
            "command": r"V:\Project Eagle\langgraph-playground\.venv\Scripts\python.exe",
            "args": [
                r"V:\Project Eagle\langgraph-playground\17-mcp-langgraph\main.py"
            ],
        },
        "expense": {
            "transport": "streamable_http",
            "url": "https://expence-tracker-mcp-vbp.fastmcp.app/mcp"
        },
    }
)


def load_mcp_tools() -> list[BaseTool]:
    try:
        return run_async(client.get_tools())
    except Exception as e:
        print(f"Failed to load MCP tools: {e}")
        return []


mcp_tools = load_mcp_tools()

tools = [
    search_tool,
    get_stock_price,
    *mcp_tools,
]

llm_with_tools = llm.bind_tools(tools)


class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


async def chat_node(state: ChatState):
    response = await llm_with_tools.ainvoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


tool_node = ToolNode(tools)


async def init_checkpointer():
    conn = await aiosqlite.connect("chatbot.db")
    return AsyncSqliteSaver(conn)


checkpointer = run_async(init_checkpointer())


graph = StateGraph(ChatState)

graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

chatbot = graph.compile(
    checkpointer=checkpointer
)


async def stream_chat(user_input, config, output_queue):
    try:
        async for chunk, metadata in chatbot.astream(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
            stream_mode="messages",
        ):
            output_queue.put((chunk, metadata))

    except Exception as e:
        output_queue.put(("__ERROR__", e))

    finally:
        output_queue.put(("__DONE__", None))


async def get_threads():
    threads = set()

    async for checkpoint in checkpointer.alist(None):
        thread_id = checkpoint.config.get(
            "configurable", {}
        ).get("thread_id")

        if thread_id:
            threads.add(thread_id)

    return list(threads)


def retrieve_all_threads():
    return run_async(get_threads())


async def get_conversation(thread_id):
    state = await chatbot.aget_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    return state.values.get("messages", [])


def load_conversation(thread_id):
    return run_async(
        get_conversation(thread_id)
    )