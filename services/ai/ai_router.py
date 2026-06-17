from services.ai.groq_provider import GroqProvider


class AIRouter:

    @staticmethod
    def _route(provider, prompt):

        provider = provider.lower().strip()

        if provider == "groq":

            return GroqProvider.generate(prompt)

        else:

            raise Exception(f"AI provider not supported: {provider}")
