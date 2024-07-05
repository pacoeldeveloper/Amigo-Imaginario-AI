import os
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore


class GeminiController:

    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    # Generar texto a partir de entradas de texto
    def generate_text(self, prompt):
        response = self.model.generate_content(prompt)
        return response.text


if __name__ == "__main__":
    gemini_controller = GeminiController()
    print(gemini_controller.generate_text("What is the meaning of life"))
