import os
import json
from llama_cpp import Llama

# Define the path to your local model.
# Make sure you create a 'model' folder in your project's root and place the .gguf file there.
MODEL_PATH = os.path.join("model", "Meta-Llama-3-8B-Instruct.Q4_0.gguf")


def evaluate_cv_with_llama(cv_text: str) -> dict:
    """
    Analyzes the given CV text using a local Llama 3 model. The model itself
    performs the scoring and extractions, returning a structured JSON dictionary.
    The output will always be in English.
    """
    if not os.path.exists(MODEL_PATH):
        return {"error": f"Model file not found at: {MODEL_PATH}"}

    try:
        # 1. Load the Llama 3 model
        # n_ctx is the context window size. 2048 should be enough for most CVs.
        llm = Llama(model_path=MODEL_PATH, n_ctx=4096, verbose=False)

        # 2. Create the prompt using the specific Llama 3 Instruct format
        # This format is crucial for the model to understand the instructions correctly.
        system_prompt = """You are an expert HR technology assistant specializing in CV analysis. Your task is to analyze the CV text provided by the user and provide the evaluation results in a structured JSON format. The input CV text might be in any language, but your output MUST BE in English. Your response must ONLY be the required JSON object, with no other explanations or text."""

        user_prompt = f"""
        Please analyze the following CV text based on the rules I provided.

        JSON Output Instructions:
        1.  `skills_found`: Extract all technical skills (programming languages, libraries, tools, platforms, etc.) from the text as a list of strings.
        2.  `experience_years`: CALCULATE the candidate's total years of professional experience based on the dates in the text. Assume 'Present' means the current year (2025). Provide a single number as the result.
        3.  `education_level`: Identify the highest academic degree mentioned (e.g., "Bachelor's Degree", "Master's Degree", "PhD").
        4.  `summary`: Write a professional 2-3 sentence summary of the candidate's profile and areas of expertise.
        5.  `scores`: CALCULATE the scores based on the following rules:
            - `skills` (Max 50): Assign a score based on the quantity and relevance of skills for a data science role.
            - `experience` (Max 30): Assign a score based on the calculated years of experience.
            - `education` (Max 20): Assign a score based on the identified education level.
            - `total`: CALCULATE the sum of the three scores above.

        Required Output Format (Only fill this structure):
        ```json
        {{
          "skills_found": [],
          "experience_years": 0,
          "education_level": "N/A",
          "summary": "",
          "scores": {{
            "skills": 0,
            "experience": 0,
            "education": 0,
            "total": 0
          }}
        }}
        ```

        CV Text to Analyze:
        ---
        {cv_text}
        ---
        """

        # 3. Call the model to get a response
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            # We explicitly ask for a JSON response
            response_format={"type": "json_object"},
            temperature=0.2  # Lower temperature for more deterministic results
        )

        # 4. Extract and parse the JSON content
        response_text = response['choices'][0]['message']['content']
        return json.loads(response_text)

    except Exception as e:
        print(f"Llama 3 model error: {e}")
        return {"error": f"An error occurred while processing the CV with the local model: {str(e)}"}