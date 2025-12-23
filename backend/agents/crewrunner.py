# backend/crew/crew_runner.py

from crewai import Crew, Process
from crewai.project import CrewBase


@CrewBase
class CaseCopilotCrew:
    """
    Crew definition for Case-Copilot.
    Agents and tasks are loaded automatically from YAML configs.
    """

    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,   # auto-loaded
            tasks=self.tasks,     # auto-loaded
            process=Process.sequential,
            verbose=True
        )
