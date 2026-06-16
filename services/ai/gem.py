import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")

class GeminiProvider:

    @staticmethod
    def chat(prompt: str):
        response = model.generate_content(prompt)
        return response.text