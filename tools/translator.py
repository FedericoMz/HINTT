import os
import base64
import ollama
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from io import BytesIO
from PIL import Image
from mss.base import ScreenShot
from openai import OpenAI
from tools.logger import logger

load_dotenv(dotenv_path="config.env")


class History:
    def __init__(self):
        self.logger = logger
        self.previous_messages = []

    def add(self, new_element):
        max_length = int(os.getenv("CONTEXT_LENGTH", "5"))
        self.previous_messages.insert(0, new_element)
        if len(self.previous_messages) > max_length:
            self.previous_messages.pop()
        logger.debug(f"Updated history: {self.previous_messages}")


class BaseTranslator(ABC):
    def __init__(self):
        self.history = History()
        self.logger = logger

    @abstractmethod
    def translate_image(self, screenshot):
        pass

    def _convert_screenshot(self, screenshot: ScreenShot):
        img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        base64_image = base64.b64encode(buffered.getvalue()).decode("utf-8")

        self.logger.debug("Screenshot successfully converted to base64.")
        return base64_image


class OpenAITranslator(BaseTranslator):
    def __init__(self):
        super().__init__()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            self.logger.error("OPENAI_API_KEY variable is not set.")
            raise ValueError("OPENAI_API_KEY variable is not set.")
        self.client = OpenAI(api_key=api_key)

    def translate_image(self, screenshot: ScreenShot) -> str:
        base64_image = self._convert_screenshot(screenshot)
        context = "\n".join(self.history.previous_messages)
        prompt = os.getenv("PROMPT", "") + f' Previously translated text for context: {context}'
        self.logger.info("Sending image for translation...")

        try:
            response = self.client.responses.create(
                model=os.getenv("OPENAI_MODEL"),
                temperature=0,
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        ],
                    }
                ],
            )
            self.history.add(response.output_text)
            self.logger.info("Translation successful!")
            return response.output_text
        except Exception as e:
            self.logger.exception("Error during translation with OpenAI.")
            return f"Error during translation: {e}"


class OllamaTranslator(BaseTranslator):
    def __init__(self):
        super().__init__()

    def translate_image(self, screenshot: ScreenShot) -> str:
        base64_image = self._convert_screenshot(screenshot)
        context = "\n".join(self.history.previous_messages)
        prompt = os.getenv("PROMPT", "") + f' Previously translated text for context: {context}'
        self.logger.info("Sending image for translation...")

        try:
            response = ollama.chat(
                model="llava",
                options={
                    'temperature': 0
                },
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [base64_image]
                    }
                ]
            )
            self.history.add(response.message.content)
            self.logger.info("Translation successful!")
            return response.message.content
        except Exception as e:
            self.logger.exception("Error during translation with Ollama.")
            return f"Error during translation: {e}"
