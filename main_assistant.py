import os
import sys
import argparse
from dotenv import load_dotenv

load_dotenv()  # loads OPENAI_API_KEY, etc.

from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
# your custom tools import…
from custom_tools import (
    apify_search_tool,
    google_trends_tool,
    pytrends_tool,
    calendar_tools,
    financial_datasets_tools,
    gmail_tools,
)

# 1) Aggregate all tools into a single list
tools = [
    apify_search_tool.tool,
    google_trends_tool.tool,
    pytrends_tool.tool,
] + calendar_tools.tools + financial_datasets_tools.tools + gmail_tools.tools

# 2) Spin up your LLM
llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")

# 3) Create the tool-calling agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,  # official “functions” agent
    verbose=True,
)

def main():
    parser = argparse.ArgumentParser(
        description="Run the assistant agent with a given prompt."
    )
    parser.add_argument(
        "text",
        help="The prompt text to send to the agent",
        type=str
    )
    args = parser.parse_args()

    # run the agent on the user-provided prompt
    result = agent.run(args.text)
    print(result)

if __name__ == "__main__":
    main()
