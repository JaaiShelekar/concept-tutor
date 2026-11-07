
import os
import time
from google import genai
from google.genai import types


class GeminiTutor:
    def __init__(self):
        key = os.getenv("GEMINI_API_KEY")

        if not key:
            raise RuntimeError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        self.client = genai.Client(api_key=key)
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

    def generate(
        self,
        prompt,
        temperature=0.4,
        image_bytes=None,
        image_mime_type="image/png"
    ):
        start = time.perf_counter()

        contents = [prompt]

        # Add image if supplied
        if image_bytes:
            image_part = types.Part.from_bytes(
                data=image_bytes,
                mime_type=image_mime_type
            )
            contents.append(image_part)

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=float(temperature)
            )
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text, time.perf_counter() - start

    def chat(self, history):
        start = time.perf_counter()

        contents = []

        for item in history[-20:]:
            role = "user" if item["role"] == "user" else "model"

            contents.append(
                types.Content(
                    role=role,
                    parts=[
                        types.Part.from_text(text=item["content"])
                    ]
                )
            )

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.4
            )
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text, time.perf_counter() - start
