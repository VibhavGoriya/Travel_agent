from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from web_search_agent.agent import web_search_agent
from callbacks import  (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)

from dotenv import load_dotenv
load_dotenv()
scout = Agent(
    model='gemini-2.5-flash',
    name='scout',
    description='finds relevent tourism destinations.',
    instruction="""
You are destination scout.
Based on user location and vibe return top 5 places to visit. use web_search_agent tool. 
""",
        tools=[AgentTool(web_search_agent)],
        before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
