from openai import OpenAI

if __name__ == "__main__":
    client = OpenAI()

    response = client.responses.create(
        model = 'gpt-5.1',
        input = 'Hi, my name is Maliheh'
    )

    print(response.output_text)
