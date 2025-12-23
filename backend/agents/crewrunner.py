# backend/crew/crew_runner.py

from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os
from dotenv import load_dotenv

load_dotenv()


@CrewBase
class CaseCopilotCrew:
    """
    Crew definition for Case-Copilot.
    Agents and tasks are loaded automatically from YAML configs.
    """

    agents_config = "agents.yaml"
    tasks_config = "tasks.yaml"

    def __init__(self):
        # 2. Initialize the local LLM using your .env variables
        # This prevents the agents from defaulting to OpenAI
        self.ollama_llm = LLM(
            model=os.getenv("LLM_MODEL", "ollama/gemma3:1b"),  # Fallback if env is missing
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )

    # --- Agents ---
    @agent
    def input_parser(self) -> Agent:
        return Agent(
            config=self.agents_config['input_parser'],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def testcase_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['testcase_creator'],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def reviewer(self) -> Agent:
        return Agent(
            config=self.agents_config['reviewer'],
            llm=self.ollama_llm,
            verbose=True
        )

    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            llm=self.ollama_llm,
            verbose=True
        )
    # --- Tasks ---
    @task
    def clean_acceptance_criteria(self) -> Task:
        return Task(config=self.tasks_config['clean_acceptance_criteria'])

    @task
    def generate_test_cases(self) -> Task:
        return Task(config=self.tasks_config['generate_test_cases'])

    @task
    def review_test_cases(self) -> Task:
        return Task(config=self.tasks_config['review_test_cases'])

    @task
    def validate_csv_output(self) -> Task:
        return Task(config=self.tasks_config['validate_csv_output'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,   # auto-loaded
            tasks=self.tasks,     # auto-loaded
            process=Process.sequential,
            verbose=True
        )
