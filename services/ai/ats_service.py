import json
from services.ai.ai_router import AIRouter

class ATSService:

    @staticmethod
    def calculate(provider, resume_text, job_description):

        prompt = f"""
        You are an ATS scoring system.

        Return ONLY valid JSON:

        {{
          "score": 0-100,
          "matched_keywords": [],
          "missing_keywords": [],
          "suggestions": []
        }}

        RESUME:
        {resume_text}

        JOB DESCRIPTION:
        {job_description}
        """

        response = AIRouter._route(provider, prompt)

        try:
            return json.loads(response)
        except:
            return {
                "score": 0,
                "matched_keywords": [],
                "missing_keywords": [],
                "suggestions": [response]
            }
    
    