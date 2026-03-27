from google.adk.agents.llm_agent import Agent
from google.adk.tools import AgentTool
from web_search_agent.agent import web_search_agent
from callbacks import  (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)


from dotenv import load_dotenv
load_dotenv()
transport = Agent(
    model='gemini-2.5-flash',
    name='transport',
    description='Finds best transport methods.',
    instruction="""Role:
        You are the Transport Navigator, a logistics expert specializing in transit efficiency and global connectivity.
        Your goal is to solve the "last mile" problem, ensuring the traveler has a seamless transition between airports, 
        hotels, and activities. You use the web_search_agent tool to verify real-time transit availability, strikes, or recent price hikes.

      """,
    tools=[AgentTool(web_search_agent)],
    before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
