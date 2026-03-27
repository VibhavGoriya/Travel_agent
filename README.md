# Travel_agent

Intelligent Travel Planner

A multi-agent travel orchestration system built using the Google Agent Development Kit (ADK) and Gemini 2.5 Flash. This project automates complex travel research and planning by coordinating specialized AI agents.
The system uses a hierarchical multi-agent architecture to process user travel requests. A central Root Agent manages session state and memory, delegating tasks to specialized sub-agents that perform web searches, weather lookups, and financial analysis to build a comprehensive itinerary.

Multi-Agent Architecture
Root Agent: The primary coordinator that maintains user context and orchestrates the workflow between specialized agents.

Scout Agent: Recommends destinations based on user preferences and vibes.

Transport Agent: Plans logistics, including flight routes, train connections, and local transit from the user's origin.

Market Analyst: Performs real-time price discovery and budget forecasting.

Agent Skills Integration
This project utilizes the ADK Skills feature to encapsulate complex response templates and behavioral logic into modular components. These skills ensure consistent, structured outputs across the system:

scout.py: Integrates destination-matching-skill for curated recommendations.

transport.py: Integrates transit-logistics-skill for detailed route planning.

market_analyst.py: Integrates budget-estimation-skill for categorized financial breakdowns.

External Tools and MCP Migration

External capabilities are currently implemented as native Python functions in mcp_tools.py. These tools provide real-time data for weather (via Open-Meteo) and currency conversion (via Frankfurter API).
The tools in mcp_tools.py are built with strict type-hinting and standardized docstrings, making them fully compatible with the Model Context Protocol (MCP).The architecture is designed to allow shifting these capabilities to a standalone FastMCP server. This will decouple the tool execution from the main application, allowing the travel capabilities to be served as an independent resource to any MCP-compatible client (e.g., Claude Desktop, Cursor, or other AI agents).

Tech Stack
Framework: Google ADK v1.27+

Model: Gemini 2.5 Flash

API Layer: FastAPI

Database: SQLite (via DatabaseSessionService)

