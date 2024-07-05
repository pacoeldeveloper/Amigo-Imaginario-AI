import os
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore


class GeminiController:

    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)

    # Generar modelo
    def generate_chat_session(self, behaviour="", prevHistory=[]):
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction=behaviour,
        )

        self.chat_session = model.start_chat(history=prevHistory)

    # Generar texto a partir de entradas de texto
    def generate_text(self, prompt, behaviour="", prevHistory=[]):
        self.generate_chat_session(behaviour, prevHistory)
        response = self.chat_session.send_message(prompt)
        return response.text


if __name__ == "__main__":
    # Ejemplo
    gemini_controller = GeminiController()
    print(
        gemini_controller.generate_text(
            "What is the meaning of life", "Behave as a scientist"
        )
    )
