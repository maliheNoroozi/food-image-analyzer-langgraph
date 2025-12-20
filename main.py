from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()

    model = "gpt-5.1"
    history = []

    while True:
        user_prompt = input("You: ")

        if user_prompt.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break

        history.append({"role": "user", "content": user_prompt})

        response = client.responses.create(model=model, input=history)

        assistant_response = response.output_text
        history.append({"role": "assistant", "content": assistant_response})

        print(f"Assistant: {assistant_response}")
