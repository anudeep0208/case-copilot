# backend/main.py (Updated with Mock Logic)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import time  # Import time for a simulated agent delay


# --- Mock Function Definition ---
def mock_test_case_generator(story_id: str, criteria: str, test_type: str) -> str:
    """
    MOCK FUNCTION: Simulates the agent system and returns a hardcoded CSV string.
    Includes a 3-second delay to test the frontend's loader/spinner display.
    """
    time.sleep(3)  # Simulate the time it takes for agents to generate cases

    # Use the input variables in the CSV data to confirm data flow is working
    mock_csv_data = (
        "Name,Description,Pre-Conditions,Steps,Expected Result,Priority,UserStoryID\n"
        f"MOCK Test Case 1: Positive Flow ({test_type}),Verify main success path based on criteria: '{criteria[:40]}...',"
        "User is logged in.,1. Input valid data. 2. Click submit. 3. Verify success message.,The expected action is completed successfully.,High,{story_id}\n"
        f"MOCK Test Case 2: Negative Flow ({test_type}),Verify error handling when submitting invalid data.,User is on the form.,1. Input invalid data (e.g., empty field). 2. Click submit.,A clear validation error message is displayed.,High,{story_id}\n"
        f"MOCK Test Case 3: Edge Case (Type: {test_type}),Verify system handling of extreme values or limits.,User is viewing the list.,1. Load the maximum number of items (1000). 2. Check performance.,The system loads within 2 seconds with no errors.,Medium,{story_id}\n"
    )
    return mock_csv_data


# ------------------------------

app = FastAPI(title="Case Co-Pilot API", version="1.0.0")

# --- CORS Configuration (Same) ---
origins = [
    "http://127.0.0.1:5500",  # Your Live Server URL for development
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
    test_type: str = "Functional"  # Default value


# --- API Endpoint Definition (UPDATED) ---
@app.post("/generate")
async def generate_tests(request: StoryRequest):
    """
    Handles the test case generation request using the temporary mock function.
    """
    try:
        # --- MOCK FUNCTION CALL FOR TESTING ---
        csv_content = mock_test_case_generator(
            request.story_id,
            request.criteria,
            request.test_type
        )
        # -------------------------------------

        # This will return a dictionary with the mock CSV data
        return {"status": "success", "csv_data": csv_content}

    except Exception as e:
        print(f"An error occurred: {e}")
        # Return a 500 status code with a helpful error message for the frontend
        raise HTTPException(
            status_code=500,
            detail=f"Internal Server Error: {e}"
        )

# To run this file: uvicorn main:app --reload