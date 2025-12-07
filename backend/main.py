# backend/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# --- NEW IMPORT ---
from mock_generator import mock_test_case_generator

# ------------------

app = FastAPI(title="Case Co-Pilot API", version="1.0.0")

# --- CORS Configuration ---
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request Body Schema (Same) ---
class StoryRequest(BaseModel):
    story_id: str
    criteria: str
    test_type: str = "Functional"
    email: str = ""


# --- API Endpoint Definition ---
@app.post("/generate")
async def generate_tests(request: StoryRequest):
    """
    Handles the test case generation request using the temporary mock function.
    """
    print(f"Received request for {request.story_id}. Type: {request.test_type}. Owner: {request.email}")

    try:
        # Call the MOCK FUNCTION imported from mock_generator.py
        csv_content = mock_test_case_generator(
            request.story_id,
            request.criteria,
            request.test_type,
            request.email
        )

        # Return the raw CSV string in the required 'csv_data' key
        return {"status": "success", "csv_data": csv_content}

    except Exception as e:
        print(f"An error occurred: {e}")
        # Ensure error handling returns a 500 status
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {e}"
        )

# To run this file: uvicorn main:app --reload