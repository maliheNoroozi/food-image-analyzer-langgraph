from openai import OpenAI
from opik.integrations.openai import track_openai
from pydantic import BaseModel

from services.chat_gpt.config import DEFAULT_CHATGPT_MODEL


class ChatGPT:
    def __init__(self):
        self.client = track_openai(OpenAI())

    def generate_text_response(
        self, user_prompt: str, model: str = DEFAULT_CHATGPT_MODEL
    ) -> str:
        response = self.client.responses.create(model=model, input=user_prompt)
        return response.output_text

    def generate_parsed_response(
        self,
        system_prompt: str,
        user_prompt: str,
        response_format: BaseModel,
        model: str = DEFAULT_CHATGPT_MODEL,
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
        system_prompt: str,
        user_prompt: str,
        image_url: str,
        response_format: BaseModel,
        model: str = DEFAULT_CHATGPT_MODEL,
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
        system_prompt: str,
        user_prompt: str,
        base64_image: str,
        response_format: BaseModel,
        model: str = DEFAULT_CHATGPT_MODEL,
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
