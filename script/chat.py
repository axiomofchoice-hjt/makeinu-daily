from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
from typing import List


class Chat:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        self.messages: List[ChatCompletionMessageParam] = []

    def call(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        response = (
            self.client.chat.completions.create(
                model="deepseek-chat",
                messages=self.messages,
                stream=False,
            )
            .choices[0]
            .message
        )
        assert response.role == "assistant"
        assert response.content is not None
        self.messages.append({"role": response.role, "content": response.content})
        return response.content

    def clear(self):
        self.messages = []
