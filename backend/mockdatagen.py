# backend/mock_generator.py

import time


def mock_test_case_generator(story_id: str, criteria: str, test_type: str, email: str) -> str:
    """
    MOCK FUNCTION: Simulates the agent system by returning a CSV string
    with Rally-like headers and injected user data.
    """
    time.sleep(3)  # Simulate the time it takes for agents to generate cases

    # Use a default email if none is provided, as allowed by the frontend validation
    owner_email = email if email else "mock.owner@company.com"

    # Headers matching the user's requested keys for Rally/Agile Central import
    csv_headers = "Object Type,Name,Description,Owner,Type,Method,Workproduct\n"

    # Mock Data Rows
    # The data for each row is structured using the new fields and injected with user variables
    mock_csv_data = (
        f'Test Case,TC-{story_id}-001: Positive Flow,'
        f'Verify the main success path based on criteria: "{criteria[:40]}...",'
        f'{owner_email},'
        f'{test_type},'
        f'Manual,'
        f'{story_id}\n'

        f'Test Case,TC-{story_id}-002: Negative - Invalid Input,'
        f'Verify system response when invalid data is entered (e.g., empty fields or non-numeric),'
        f'{owner_email},'
        f'{test_type},'
        f'Manual,'
        f'{story_id}\n'

        f'Test Case,TC-{story_id}-003: Edge Case - Security,'
        f'Verify that the system handles a cross-site scripting attempt in the criteria field,'
        f'{owner_email},'
        f'{test_type},'
        f'Manual,'
        f'{story_id}\n'
    )

    return csv_headers + mock_csv_data