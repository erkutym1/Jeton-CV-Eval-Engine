import os
import json
from google import genai
from google.genai import types

try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Could not initialize Gemini Client. Make sure GEMINI_API_KEY is set. Error: {e}")
    client = None

MODEL_NAME = "gemini-2.5-pro"

def evaluate_cv_with_gemini(cv_text: str) -> dict:
    """
    Analyzes a single CV to extract basic information and calculates an overall score
    based on the 50 (skills) / 30 (experience) / 20 (education) rule.
    """
    if not client:
        return {"error": "Gemini Client could not be initialized."}
    try:
        prompt = f"""
        You are an expert HR analyst. Your task is to analyze the following CV text and provide a structured evaluation. Your response MUST ONLY be a JSON object. The output MUST BE in English. If a field cannot be found, use "N/A" or 0.

        Follow these scoring rules precisely:
        1.  Extract `candidate_name`, `contact_email`, `experience_years`, `education_level`, and a list of `skills_found`.
        2.  Calculate a score for each category:
            - `skills` (Max 50 points): Score based on the quantity and relevance of data skills.
            - `experience` (Max 30 points): Score based on the total years of experience. (e.g., 0-2 years: 5-10 pts, 3-5 years: 15-20 pts, 6+ years: 25-30 pts).
            - `education` (Max 20 points): Score based on degree level. (e.g., Bachelor's: 10, Master's: 15, PhD: 20).
        3.  `total` score MUST be the sum of the three category scores.

        Required JSON Structure:
        {{
          "candidate_name": "Full Name",
          "contact_email": "email@example.com",
          "experience_years": 5,
          "education_level": "Master's Degree",
          "skills_found": ["Python", "SQL", "TensorFlow"],
          "summary": "A 2-3 sentence summary of the candidate's profile.",
          "scores": {{
            "skills": 40,
            "experience": 20,
            "education": 15,
            "total": 75
          }}
        }}

        CV Text to Analyze:
        ---
        {cv_text}
        ---
        """
        config = types.GenerateContentConfig(response_mime_type="application/json")
        response = client.models.generate_content(model=f'models/{MODEL_NAME}', contents=prompt, config=config)
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API error (evaluation): {e}")
        return {"error": f"An error occurred while processing the CV: {str(e)}"}