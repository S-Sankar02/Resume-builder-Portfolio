import json

from services.ai.ai_router import AIRouter


class ATSService:

    @staticmethod
    def calculate(provider, resume_text, job_description):

        prompt = f"""

You are an ATS Resume Analyzer.

Compare resume with job description.

Give ATS score from 0 to 100.

Return ONLY valid JSON.

Format:

{{
 "score":0,
 "matched_keywords":[],
 "missing_keywords":[],
 "analysis":"",
 "suggestions":[]
}}



RESUME:

{resume_text}



JOB DESCRIPTION:

{job_description}

"""

        response = AIRouter._route(provider, prompt)

        try:

            return json.loads(response)

        except Exception:

            try:

                cleaned = response.replace("```json", "").replace("```", "").strip()

                return json.loads(cleaned)

            except:

                return {
                    "score": 0,
                    "matched_keywords": [],
                    "missing_keywords": [],
                    "analysis": response,
                    "suggestions": [],
                }
