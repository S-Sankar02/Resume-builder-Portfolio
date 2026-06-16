from services.ai.openai_provider import OpenAIProvider
from services.ai.gem import GeminiProvider

class AIRouter:

    @staticmethod
    def _route(provider, prompt):

        if provider == "openai":
            return OpenAIProvider.chat(prompt)

        if provider == "gemini":
            return GeminiProvider.chat(prompt)

        # AUTO MODE
        if len(prompt) > 1500:
            return GeminiProvider.chat(prompt)

        return OpenAIProvider.chat(prompt)

    @staticmethod
    def generate_summary(provider, name, role, skills):
        prompt = f"""
        Write a professional ATS-friendly resume summary.

        Name: {name}
        Role: {role}
        Skills: {', '.join(skills)}

        Keep it short and impactful.
        """
        return AIRouter._route(provider, prompt)

    @staticmethod
    def improve_bullet(provider, text):
        prompt = f"""
        Improve this resume bullet point:
        {text}

        Make it professional and result-oriented.
        """
        return AIRouter._route(provider, prompt)

    @staticmethod
    def job_tailor(provider, resume, job_desc):
        prompt = f"""
        Tailor this resume for the job description.

        RESUME:
        {resume}

        JOB DESCRIPTION:
        {job_desc}

        Improve ATS keywords and structure.
        """
        return AIRouter._route(provider, prompt)
    