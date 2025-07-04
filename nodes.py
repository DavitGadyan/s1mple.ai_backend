import os
from dotenv import load_dotenv

load_dotenv()

from react import react_agent_runnable, tools
from state import AgentState
from langchain_core.agents import AgentFinish

# Reasoning engine accepts extra kwargs (like tools) but only uses state
# This prevents errors when the graph runner passes in the tools list.

def run_agent_reasoning_engine(state: AgentState, **kwargs):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}

# Custom tool execution logic replacing ToolExecutor

def execute_tools(state: AgentState, tools):
    agent_action = state["agent_outcome"]
    tool_name = getattr(agent_action, "tool", None)
    tool_input = getattr(agent_action, "tool_input", None)

    if not tool_name:
        return {"intermediate_steps": [(agent_action, "No tool to execute.")]}

    # Find and invoke the matching tool
    for tool in tools:
        if getattr(tool, "name", None) == tool_name:
            try:
                result = tool.run(tool_input)
            except Exception as e:
                result = f"Error running tool '{tool_name}': {e}"
            break
    else:
        result = f"Tool '{tool_name}' not found."

    return {"intermediate_steps": [(agent_action, str(result))]}
