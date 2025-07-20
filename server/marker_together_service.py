import os
import together

class TogetherService:
    def __init__(self, model="meta-llama/Llama-3-8b-chat-hf"):
        self.api_key = os.getenv("TOGETHER_API_KEY")
        if not self.api_key:
            raise EnvironmentError("Missing TOGETHER_API_KEY")
        together.api_key = self.api_key
        self.model = model

    def __call__(self, prompt: str, **kwargs) -> str:
        response = together.Complete.create(
            model=self.model,
            prompt=prompt,
            max_tokens=2048,
            temperature=0.7
        )
        return response["output"]["choices"][0]["text"]
