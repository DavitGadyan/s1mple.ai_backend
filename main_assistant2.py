import os
from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_core.prompts import ChatPromptTemplate

# Import your custom tools

from custom_tools import (
    apify_search_tool,
    google_trends_tool,
    pytrends_tool,
    calendar_tools,
    financial_datasets_tools,
    gmail_tools,
)

# Aggregate all tools into a single list
tools = [
    apify_search_tool.tool,
    google_trends_tool.tool,
    pytrends_tool.tool,
] + calendar_tools.tools + financial_datasets_tools.tools + gmail_tools.tools

# 2) Spin up your LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

# 3) Define the ChatPromptTemplate with placeholders for history & scratchpad
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use your tools to fulfill user requests."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4) Create the tool-calling agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # ← official “functions” agent
    verbose=True,
)



if __name__ == "__main__":
    res = agent.run(
            "Find information about David Gadyan on LinkedIn, "
            # "then add calendar meeting at 3 pm today with David"
            "then send an email with the findings of personal info to davidgadyan92@gmail.com"
        )
    print("Final output:", res)
