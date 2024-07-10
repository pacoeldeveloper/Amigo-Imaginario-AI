import os
import google.generativeai as genai  # type: ignore
from dotenv import load_dotenv  # type: ignore

class GeminiController:

    def __init__(self):
        load_dotenv()
        GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=GEMINI_API_KEY)

    # Generar modelo
    def generate_chat_session(self, behaviour=None, prevHistory=[]):
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
    def generate_text(self, prompt, behaviour=None, prevHistory=[]):
        self.generate_chat_session(behaviour, prevHistory)
        response = self.chat_session.send_message(prompt)
        return response.text

    # Generar behaviour a partir de respuestas
    def generate_behaviour(self, userPreferences):
        prompt = ("This are the answers for an imaginary friend app, where the user \
            can interact with an imaginary friend. The user can create an imaginary \
                friend based on the answers of this initial questions.\n" 
        + str(userPreferences) + "\nGenerate behaviour (prompt) based on the answers of the \
            user so the imaginary friend can behave as the user wants.")
        
        self.generate_chat_session()
        response = self.chat_session.send_message(prompt)
        return response.text


if __name__ == "__main__":
    # Ejemplo
    gemini_controller = GeminiController()

    userPreferences = '''
    [{
    "How old is your friend?": 15 
    }, 
    {
    "What does your friend like to do?": ["Play basketball", "Play videogames", "Read fantasy books"]
    },
    {
    "What is your friend's favorite food?": ["Pizza", "Lasagna"]
    },
    {
    "What is your friend's favorite color?": ["Blue"]
    }]'''

    exampleBehaviour = gemini_controller.generate_behaviour(userPreferences)

    print(exampleBehaviour) # Muestra el prompt general

    print(
        gemini_controller.generate_text(
            "What is your favorite thing to do in the summer?", exampleBehaviour
        )
    ) 
