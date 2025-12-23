import os
from dotenv import load_dotenv
from backend.agents.kickoff import kickoff_case_copilot

# 1. Load your API keys (ensure you have a .env file with OPENAI_API_KEY)
load_dotenv()


def run_testcase_agent(story_id: str, criteria: str, test_type: str) -> str:
    """
    Wrapper function to align with your requested test format.
    Note: story_id and test_type are passed for context, but the current
    crew logic primarily processes the 'criteria'.
    """
    print(f"--- Processing {story_id} ({test_type} Testing) ---")

    # Calls your existing kickoff logic
    result = kickoff_case_copilot(acceptance_criteria=criteria)

    # Return the raw string output from the Crew
    #return result.raw if hasattr(result, 'raw') else str(result)
    print("DEBUG RESULT TYPE:", type(result))
    print("DEBUG RESULT:", result.raw)

    #return str(result)
    return result.raw


if __name__ == "__main__":
    # SAMPLE INPUT: A messy string with noise to test the sanitization logic
    messy_criteria = """
    **User Story:** As a user, I want to reset my password.
    - User clicks 'Forgot Password' link [http://internal-dev-link.com/reset/debug].
    - System sends email with a 6-digit code.
    - !IMAGE_BLOB_001! (Screenshot of the UI goes here)
    - User enters code and new password.
    - Password must be 8 characters.
    - Error should show if code is expired: https://docs.errorcodes.io/403
    """

    output = run_testcase_agent(
        story_id="US123565",
        criteria=messy_criteria,
        test_type="Functional"
    )

    print("\n" + "=" * 21 + " CREWAI OUTPUT " + "=" * 21)
    print(output)
    print("=" * 57)