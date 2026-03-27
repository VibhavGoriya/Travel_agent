from google.adk.agents.llm_agent import Agent
from google.adk.skills import models
from google.adk.tools import skill_toolset, AgentTool, FunctionTool
from web_search_agent.agent import web_search_agent
from mcp_tools import convert_currency
from callbacks import (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)
from dotenv import load_dotenv

load_dotenv()

# Define the Skill
budget_estimation_skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="budget-estimation-skill",
        description="Calculates trip costs, breaks down expenses, and evaluates financial feasibility.",
    ),
    instructions="""
# Budget Estimation Response Template

Use this template when the user asks for trip costs, budget breakdowns, or wants to know if a specific trip is feasible within their financial constraints.

## Base Template
`{acknowledgment_line} {high_level_estimate} {breakdown_section} {saving_tip_line} {next_step_line}`

## Placeholder Guidance
- `{acknowledgment_line}`: A brief validation of the user's trip idea.
- `{high_level_estimate}`: The total estimated cost range based on their persona.
- `{breakdown_section}`: A concise, bulleted list dividing the total into major categories (Flights, Accommodation, Food, Transit).
- `{saving_tip_line}`: One actionable, highly specific tip to reduce costs.
- `{next_step_line}`: A closing question to move the planning forward.

## Style Rules
- Be realistic, not absolute. Always use ranges.
- Do not promise that prices will remain the same.
- Constructive honesty: If a budget is too low, gently state it immediately and offer alternatives.
"""
)

# Package into a Toolset
market_analyst_skillset = skill_toolset.SkillToolset(skills=[budget_estimation_skill])

# Instantiate the Agent
market_analyst = Agent(
    model='gemini-2.5-flash',
    name='market_analyst',
    description='Planning the finance of the trip carefully.',
    instruction="""Role:
    You are the Market Analyst for an intelligent travel system.
    Your specialty is real-time price discovery and budget forecasting. 
    Use the web_search_agent tool to find current market rates for flights and hotels.
    Use the convert_currency tool to ensure the user's budget matches the destination's local currency.
    Always format your final output strictly according to your budget-estimation-skill.
    """,
    tools=[market_analyst_skillset, AgentTool(web_search_agent), FunctionTool(convert_currency)],
    before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
