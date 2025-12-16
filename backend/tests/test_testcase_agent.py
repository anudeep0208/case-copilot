from backend.agents.testcase_agent import run_testcase_agent

if __name__ == "__main__":
    output = run_testcase_agent(
        story_id="US123",
        criteria="User should be able to log in with valid credentials",
        test_type="Functional"
    )

    print("----- CREWAI OUTPUT -----")
    print(output)
    print("-------------------------")
