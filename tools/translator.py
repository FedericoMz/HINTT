import os
from openai import OpenAI

class LLMTranslator:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY variable is not set.")
        self.client = OpenAI(api_key=api_key)

    def translate_image(self, base64_image: str) -> str:
        try:
            response = self.client.responses.create(
                model="gpt-4.1",
                temperature=0,
                input=[
                    {
                        "role": "user",
                        "content": [
                            { "type": "input_text", "text": "What is the translation of the text? Just provide a natural translation, without any comment and without the original text"},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    }
                ],
            )
            return response.output_text
        except Exception as e:
            return f"Error during translation: {e}"
