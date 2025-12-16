from crewai import Agent, Task, Crew
from crewai.llm import LLM
from dotenv import load_dotenv
import os


load_dotenv()
LLM_MODEL = os.getenv("LLM_MODEL")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")


ollama_llm = LLM(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL
)


def run_testcase_agent(story_id: str, criteria: str, test_type: str) -> str:
    agent = Agent(
        role="QA Test Case Generator",
        goal="Generate clear and structured test cases",
        backstory=(
            "You are a senior QA engineer with experience in "
            "functional, regression, and UAT testing."
        ),
        llm= ollama_llm,
        verbose=False
    )

    task = Task(
        description=(
            f"Generate 2 {test_type} test cases.\n\n"
            f"Story ID: {story_id}\n"
            f"Acceptance Criteria:\n{criteria}"
        ),
        agent=agent,
        expected_output="A list of test cases."
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )

    return str(crew.kickoff())
