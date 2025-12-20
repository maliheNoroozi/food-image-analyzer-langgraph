from openai import OpenAI
from pydantic import BaseModel


class ChatGPT:
    def __init__(self):
        self.client = OpenAI()

    def generate_text_response(self, model: str, user_prompt: str):
        response = self.client.responses.create(model=model, input=user_prompt)
        return response.output_text

    def generate_parsed_response(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        response_format: BaseModel,
    ) -> BaseModel:
        response = self.client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            text_format=response_format,
        )
        return response.output_parsed

    def generate_image_response_by_image_url(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        image_url: str,
        response_format: BaseModel,
    ) -> BaseModel:
        response = self.client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_prompt},
                        {"type": "input_image", "image_url": image_url},
                    ],
                },
            ],
            text_format=response_format,
        )
        return response.output_parsed

    def generate_image_response_by_base64_image(
        self,
        model: str,
        system_prompt: str,
        user_prompt: str,
        base64_image: str,
        response_format: BaseModel,
    ) -> BaseModel:
        response = self.client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": user_prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    ],
                },
            ],
            text_format=response_format,
        )
        return response.output_parsed
