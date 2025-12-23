# backend/runner/kickoff.py

from backend.agents.crewrunner import CaseCopilotCrew

def kickoff_case_copilot(acceptance_criteria: str) -> str:
    """
    Entry point to run CaseCopilot.
    """
    crew = CaseCopilotCrew()
    result = crew.crew().kickoff(inputs={
        "acceptance_criteria": acceptance_criteria
    })
    return result
