from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget
from dotenv import load_dotenv
import os
from test_auto import run_automated_tests
import logging
from datetime import datetime

load_dotenv()

# === CẤU HÌNH LOGGING ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("test_results.log", encoding="utf-8"),  # File log chung
        logging.StreamHandler()  # Hiển thị ra console
    ]
)
logger = logging.getLogger("TravelBuddy-Agent")

# 1. Đọc System Prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

# 2. Khai báo State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

# 3. Khởi tạo LLM và Tools
tools_list = [search_flights, search_hotels, calculate_budget]
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://kelkoo-her-murphy-rank.trycloudflare.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
llm = ChatOpenAI(
    base_url=f"{OLLAMA_BASE_URL}",  
    api_key=OLLAMA_API_KEY,                 
    model=MODEL_NAME,
    temperature=0.0,
)

llm_with_tools = llm.bind_tools(tools_list)

# 4. Agent Node
def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages

    # Log input message
    user_message = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
    logger.info(f"Input từ user: {user_message}")

    response = llm_with_tools.invoke(messages)

    # === LOGGING CHI TIẾT ===
    if response.tool_calls:
        logger.warning(f"Agent quyết định gọi {len(response.tool_calls)} tool(s)")
        for i, tc in enumerate(response.tool_calls, 1):
            tool_name = tc['name']
            tool_args = tc['args']
            logger.warning(f"   [{i}] Tool: {tool_name}")
            logger.warning(f"       Tham số: {tool_args}")
            print(f"   [{i}] Gọi tool: {tool_name}({tool_args})")
    else:
        logger.info(f"Agent trả lời trực tiếp (không gọi tool)")
        print(f"   Trả lời: {response.content[:100]}...")

    return {"messages": [response]}

# 5. Xây dựng Graph
builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)

tool_node = ToolNode(tools_list)
builder.add_node("tools", tool_node)

# TODO: Sinh viên khai báo edges
# builder.add_edge(START, ...)
# builder.add_conditional_edges("agent", tools_condition)
# builder.add_edge("tools", ...)
builder.add_edge(START, "agent")
builder.add_conditional_edges(
    "agent",
    tools_condition,          # hàm này đã return "tools" hoặc "__end__"
)
builder.add_edge("tools", "agent")


graph = builder.compile()

# 6. Chat loop
if __name__ == "__main__":
    run_automated_tests(graph)
    # print("=" * 60)
    # print("TravelBuddy - Trợ lý Du lịch Thông minh")
    # print("      Gõ 'quit' để thoát")
    # print("=" * 60)

    # while True:
    #     user_input = input("\nBạn: ").strip()
    #     if user_input.lower() in ("quit", "exit", "q"):
    #         break

    #     print("\nTravelBuddy đang suy nghĩ...")
    #     result = graph.invoke({"messages": [("human", user_input)]})
    #     final = result["messages"][-1]
    #     print(f"\nTravelBuddy: {final.content}")