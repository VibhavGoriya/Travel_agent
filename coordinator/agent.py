from google.adk.agents.llm_agent import Agent
from market_analyst.agent import market_analyst
from scout.agent import scout
from transport.agent import transport
from callbacks import  (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)

from dotenv import load_dotenv
load_dotenv()
# Refined Instructions for the Coordinator/Root Agent
COORDINATOR_INSTRUCTIONS = """
You are the Lead Travel Coordinator. Your goal is to provide a seamless, end-to-end travel planning experience by orchestrating your specialized sub-agents.

**Operational Guidelines:**
1. **Delegation First:** Do not attempt to guess travel data. 
   - First use 'scout' to find destinations and activities based on user vibes.
   - Then use 'transport' to solve all movement, flight, and transit logistics.
   -Then use 'market_analyst' to get current pricing and verify budget feasibility.

2. **Synthesis:** When sub-agents return data, do not just dump their raw outputs. Merge them into a logical flow. 
   - (e.g., If 'transport' finds a flight arriving at 2 PM, ensure 'scout' suggests evening activities near the arrival area.)

 **Final Response Structure:**
If the user is not prompting for more options or any other needs we give according to the preference memory and conflict resolution points,
else after using
the 3 sub agents we summarise and dont call them further.


**Preference Memory:** Maintain the user's persona across the conversation. If they mentioned a budget early on, ensure the 'market_analyst' is briefed on that limit.

**Conflict Resolution:** If 'market_analyst' reports a destination is over-budget, proactively ask the 'scout' for cheaper alternatives or 'transport' for more affordable transit.
"""

root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='The central coordinator for an intelligent travel planning system.',
    instruction=COORDINATOR_INSTRUCTIONS,
    sub_agents=[market_analyst, scout, transport],
    before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)