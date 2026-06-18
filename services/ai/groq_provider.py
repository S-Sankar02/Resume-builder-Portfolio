import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqProvider:

    @staticmethod
    def generate(prompt):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise Exception(
                "GROQ_API_KEY environment variable is not configured"
            )

        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content