from google.adk.agents.llm_agent import Agent
from google.adk.skills import models
from google.adk.tools import skill_toolset, AgentTool, FunctionTool
from web_search_agent.agent import web_search_agent
from mcp_tools import get_weather
from callbacks import (
    log_before_agent, log_after_agent, log_before_model, 
    log_after_model, log_before_tool, log_after_tool
)
from dotenv import load_dotenv

load_dotenv()

# Define the Skill
destination_matching_skill = models.Skill(
    frontmatter=models.Frontmatter(
        name="destination-matching-skill",
        description="Matches user preferences, vibes, and constraints to specific travel destinations.",
    ),
    instructions="""
# Destination Matching Response Template

Use this template when the user provides their preferences, vibe, or constraints, and needs curated destination recommendations.

## Base Template
`{vibe_validation} {top_recommendation} {alternative_options} {why_it_fits} {engagement_question}`

## Placeholder Guidance
- `{vibe_validation}`: Acknowledges and synthesizes the user's requested tags.
- `{top_recommendation}`: The #1 best match for their criteria, styled in bold.
- `{alternative_options}`: 1-2 backup options that offer a slightly different flavor.
- `{why_it_fits}`: A 1-2 sentence explanation of exactly why this location matches their specific persona tags.
- `{engagement_question}`: A closing prompt asking them to select a destination to investigate further.

## Style Rules
- Evocative Language: Focus on sensory details rather than generic terms.
- Direct Connections: Explicitly tie the recommendation back to a preference the user stated.
- Limit Options: Avoid providing more than 3 destinations at once.
"""
)

# Package into a Toolset
scout_skillset = skill_toolset.SkillToolset(skills=[destination_matching_skill])

# Instantiate the Agent
scout = Agent(
    model='gemini-2.5-flash',
    name='scout',
    description='Finds relevant tourism destinations.',
    instruction="""Role:
    You are a destination scout.
    Based on the user's location and vibe, return top places to visit. 
    Use the get_weather tool to check the current climate of the destination and advise the user on what to expect.
    Use the web_search_agent tool for finding specific attractions.
    Always format your final recommendations strictly according to your destination-matching-skill.
    """,
    tools=[scout_skillset, AgentTool(web_search_agent), FunctionTool(get_weather)],
    before_agent_callback=log_before_agent,
    after_agent_callback=log_after_agent,
    before_model_callback=log_before_model,
    after_model_callback=log_after_model,
    before_tool_callback=log_before_tool,
    after_tool_callback=log_after_tool,
)
