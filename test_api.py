from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import os
load_dotenv()
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "https://convinced-pediatric-spanking-wrapping.trycloudflare.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.1:8b")
llm = ChatOpenAI(
    base_url=f"{OLLAMA_BASE_URL}",   # ← Quan trọng: phải thêm /v1
    api_key="ollama",                   # bất kỳ chuỗi nào cũng được
    model=MODEL_NAME,
    temperature=0.1,
)

response = llm.invoke([HumanMessage(content="What is the capital of France?")])
print(response.content)