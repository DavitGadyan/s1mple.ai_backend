from dotenv import load_dotenv
from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI

load_dotenv()

# Import and instantiate the custom tools for the agent
from custom_tools import (
    apify_search_tool,
    google_trends_tool,
    pytrends_tool,
    calendar_tools,
    financial_datasets_tools,
    gmail_tools,
)



react_prompt: PromptTemplate = hub.pull("hwchase17/react")


# Aggregate all tools into a single list
tools = [
    apify_search_tool.tool,
    google_trends_tool.tool,
    pytrends_tool.tool,
] + calendar_tools.tools + financial_datasets_tools.tools + gmail_tools.tools


llm = ChatOpenAI(model="gpt-4o-mini")

react_agent_runnable = create_react_agent(llm, tools, react_prompt)
