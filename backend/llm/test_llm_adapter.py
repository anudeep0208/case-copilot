from backend.llm.local_llm_adapter import LocalLLMAdapter


def main():
    llm = LocalLLMAdapter(model="gemma3:1b")

    prompt = (
        "You are a QA engineer.\n"
        "Generate 2 functional test cases for login.\n"
        "Use numbered bullet points only."
    )

    response = llm.complete(prompt)

    print("----- LLM RESPONSE -----")
    print(response)
    print("------------------------")


if __name__ == "__main__":
    main()
