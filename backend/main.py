# backend/main.py

"""
Main API service for Case Co-Pilot.
Provides an endpoint to generate test cases (mock or LLM-backed based on configuration).
This file handles inbound request validation, CORS configuration, and returns CSV data to the frontend.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from backend.services.mock_service import generate_mock_testcases
from backend.services.ai_service import generate_testcases
from typing import Optional
import logging
import os



# ----------------------------------------
# FastAPI Application Initialization
# ----------------------------------------
app = FastAPI(
    title="Case Co-Pilot API",
    version="1.0.0",
    description="Backend API to generate Rally-compatible Test Cases from Acceptance Criteria."
)

# Enable logging for debugging and production monitoring
logging.basicConfig(level=logging.INFO)


# ----------------------------------------
# CORS Configuration
# Allows frontend JavaScript to communicate with backend API without blocking
# ----------------------------------------
origins = [
    "http://127.0.0.1:5500",   # Local frontend served via Live Server
    "http://localhost:5500",
    "http://127.0.0.1:63342",  # PyCharm hosted frontend
    "http://localhost:63342",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,     # Allowed domains
    allow_credentials=True,
    allow_methods=["*"],       # Allow GET, POST, DELETE, PUT, etc.
    allow_headers=["*"],       # Allow all headers including JSON content type
)


# ----------------------------------------
# Request Body Schema (Pydantic Model)
# Defines expected structure of API POST request from frontend
# Fields are optional because frontend may not send all values
# ----------------------------------------
class StoryRequest(BaseModel):
    story_id: Optional[str] = ""
    criteria: Optional[str] = ""
    test_type: Optional[str] = "Functional"
    email: Optional[str] = ""


# ----------------------------------------
# POST /generate API Endpoint
# Purpose: Accept user input and return generated test cases as CSV string
# Uses a mock generator now; will later integrate CrewAI / LLM logic
# ----------------------------------------

USE_MOCK = os.getenv("USE_MOCK_LLM").lower() == "true"
@app.post("/generate")
async def generate_tests(request: StoryRequest):
    """
    Generates Rally Test Cases based on provided Story ID, Criteria, and Test Type.
    Currently, returns simulated results using mock_generator.py.
    """

    # Sanitize / normalize values to avoid 'None' in output
    story_id = str(request.story_id or "")
    criteria = str(request.criteria or "")
    test_type = str(request.test_type or "Functional")
    email = str(request.email or "")

    # Log data to backend console for visibility and debugging
    logging.info(f"Request received -> StoryID={story_id}, Type={test_type}, Owner={email}")

    try:
        # Call mock generator (later replace with real multi-agent AI flow)
        if USE_MOCK:
            csv_content = generate_mock_testcases(
                story_id,
                criteria,
                test_type,
                email
            )
            # Return response in JSON format expected by frontend
            return {
                "status": "success",
                "csv_data": csv_content
            }
        else:
            #call real agent here
            csv_content = generate_testcases(
                story_id,
                criteria,
                test_type,
                email
            )
            # Return response in JSON format expected by frontend
            return {
                "status": "success",
                "csv_data": csv_content
            }

    except Exception as e:
        # Log issue, return structured error response to frontend
        logging.error(f"Error occurred: {e}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------------
# RUN COMMAND (for manual startup via terminal)
# ----------------------------------------
# uvicorn main:app --reload
