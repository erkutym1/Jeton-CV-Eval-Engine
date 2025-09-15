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

def get_match_score_for_role(cv_text: str, description: str) -> dict:
    """
    Analyzes a single CV against a job description to get a specific match score and reasoning.
    This is the dedicated function for the 'Dream Team' feature.
    """
    if not client:
        return {"error": "Gemini Client could not be initialized."}
    try:
        prompt = f"""
        You are an expert hiring manager. Your task is to evaluate how well a single candidate's CV matches a job description.
        Your response MUST ONLY be a JSON object with two keys: 'match_score' (a number from 0 to 100) and 'reasoning' (a concise, one or two-sentence explanation for the score).

        Job Description:
        ---
        {description}
        ---

        Candidate's CV Text:
        ---
        {cv_text}
        ---
        """
        config = types.GenerateContentConfig(response_mime_type="application/json")
        response = client.models.generate_content(model=f'models/{MODEL_NAME}', contents=prompt, config=config)
        return json.loads(response.text)
    except Exception as e:
        print(f"Gemini API error (match scoring): {e}")
        return {"error": f"An error occurred while getting the match score: {str(e)}"}