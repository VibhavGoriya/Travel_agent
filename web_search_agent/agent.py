from google.adk.agents.llm_agent import Agent
from google.adk.tools import google_search
from callbacks import  (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)

from dotenv import load_dotenv
load_dotenv()
web_search_agent = Agent(
    model='gemini-2.5-flash',
    name='web_search_agent',
    description='Web search tool.',
    instruction='Answer user questions to the best of your knowledge',
    tools=[google_search],
    before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
