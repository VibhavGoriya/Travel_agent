from fastapi import FastAPI, Request
from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from sqlalchemy import create_engine
import io
import requests
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import DatabaseSessionService
from google.adk.memory import InMemoryMemoryService
from google.genai.types import Content, Part
from coordinator.agent import root_agent
import time
import logging

# Standard Python logging setup
logging.basicConfig(level=logging.INFO)
db_url="sqlite+aiosqlite:///my_agent_data.db"
session_service=DatabaseSessionService(db_url=db_url)
memory_service=InMemoryMemoryService()
APP_NAME="travel_app"

app=FastAPI()
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    memory_service=memory_service,
    app_name=APP_NAME
    )
@app.post("/debug_response")
async def debug_response(user_message: str):
    response = await runner.run_debug(user_message)
    return {"reply":response}
@app.post("/chat")
async def chat(user_message: str, user_id: str = "default_user", session_id: str = None):
    # 1. Logic: Use provided session or create a new one immediately
    active_session_id = session_id
    
    if active_session_id:
        try:
            # Check if the session exists in the service
            await session_service.get_session(
                app_name=APP_NAME,
                user_id=user_id,
                session_id=active_session_id
            )
            print(f"Using existing session: {active_session_id}")
        except Exception:
            # If the ID doesn't exist (e.g. server restarted), force a new one
            print(f"Session {active_session_id} not found. Creating new.")
            active_session_id = None

    # 2. No session_id provided OR the one provided was invalid/not found
    if not active_session_id:
        new_session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
        )
        active_session_id = new_session.id
        print(f"Created new session: {active_session_id}")

    # 3. Standard ADK Running Logic
    new_message = Content(role="user", parts=[Part(text=user_message)])
    start_time = time.perf_counter()
    
    events = runner.run(
        user_id=user_id,
        session_id=active_session_id,
        new_message=new_message
    )
    
    final_text = ""
    usage_metadata = None
    for event in events:
        
        function_calls = event.get_function_calls()

        if event.is_final_response():
            final_text = event.content.parts[0].text
            usage_metadata = getattr(event, "usage_metadata", None)
    try:
        current_session=await session_service.get_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=active_session_id
        )
        await memory_service.add_session_to_memory(current_session)
        print(f"Memory updated for session: {active_session_id}")
    except Exception as e:
        print(f"Memory extraction failed: {e}")        
    end_time = time.perf_counter()
    duration = end_time - start_time
    
    return {
        "reply": final_text,
        "Total tokens": usage_metadata.total_token_count if usage_metadata else 0,
        "time_taken_sec": round(duration, 3),
        "session_id": active_session_id
    }