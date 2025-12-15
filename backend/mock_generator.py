# backend/mock_generator.py

"""
Mock Generator Module

This file contains placeholder logic used for testing API connectivity and frontend integration.
It generates simulated CSV test case data formatted for Rally/Agile Central import,
without involving actual AI agent processing.

This temporary logic will later be replaced by:
 - CrewAI agent execution chain
 - LLM-based test case generation from acceptance criteria
 - CSV formatter and optimizer service

For now, it ensures predictable output and UI testing support.
"""

import time


def mock_test_case_generator(story_id: str, criteria: str, test_type: str, email: str) -> str:
    """
    Generates mock CSV test case output simulating what a real test generation engine
    might produce based on inputs provided via the API.

    Parameters
    ----------
    story_id : str
        Rally User Story ID associated with the test cases.
    criteria : str
        Acceptance criteria text provided by the user.
    test_type : str
        Test category selected by the user (e.g., Functional, UAT, Regression).
    email : str
        Owner email used to assign generated test cases.

    Returns
    -------
    str
        A formatted CSV string containing mock test case rows.

    Notes
    -----
    - A 3-second delay is intentionally added to simulate real processing time,
      allowing frontend loaders/spinners to be tested visually.
    """

    # --- SIMULATED DELAY (temporarily used to test UI loaders) ---
    time.sleep(3)

    # Assign default placeholder owner email if user did not specify one
    owner_email = email if email else "mock.owner@company.com"

    # CSV header row matching expected Rally import structure
    csv_headers = "Object Type,Name,Description,Owner,Type,Method,Work Product\n"

    # Build sample mock rows (Three example test case records)
    mock_csv_rows = (
        # Positive Scenario
        f'Test Case,TC-{story_id}-001: Positive Flow,'
        f'Verify main success path using criteria snippet: "{criteria[:40]}...",'
        f'{owner_email},{test_type},Manual,{story_id}\n'

        # Negative Scenario
        f'Test Case,TC-{story_id}-002: Negative - Invalid Input,'
        f'Verify handling of incorrect/empty/invalid form inputs,'
        f'{owner_email},{test_type},Manual,{story_id}\n'

        # Security / Edge Case
        f'Test Case,TC-{story_id}-003: Edge Case - Security Validation,'
        f'Ensure system prevents script injection or unsafe content submissions,'
        f'{owner_email},{test_type},Manual,{story_id}\n'
    )

    # Return headers + constructed row data combined
    return csv_headers + mock_csv_rows
