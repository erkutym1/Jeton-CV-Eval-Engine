

# CV Evaluation Engine

The CV Evaluation Engine is a Flask-based web application designed to automate the analysis and evaluation of CVs (resumes) in PDF format. It utilizes the Gemini API for AI-powered text analysis to extract key candidate information and assess suitability based on skills, experience, and education. The application also features a "Dream Team" functionality to match candidates to job descriptions. It is containerized with Docker for easy deployment.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [Docker Deployment](#docker-deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Features
- **PDF Upload and Processing**: Upload multiple PDF CVs, securely stored and processed to extract text.
- **AI-Powered CV Evaluation**: Extracts candidate details (name, email, skills, experience, education) and scores them:
  - Skills: Up to 50 points based on data skill relevance.
  - Experience: Up to 30 points based on years (e.g., 0-2 years: 5-10, 3-5 years: 15-20, 6+ years: 25-30).
  - Education: Up to 20 points based on degree (e.g., Bachelor's: 10, Master's: 15, PhD: 20).
- **Dream Team Feature**: Matches CVs to job descriptions with a 0-100 match score and reasoning.
- **File Management**: Lists uploaded CVs, supports bulk deletion, and displays raw text with evaluations.
- **Responsive Web Interface**: Built with Flask and HTML templates.
- **Docker Support**: Containerized for consistent deployment.

## Architecture
- **Flask Backend**: Manages requests, file handling, and template rendering.
- **Gemini API**: Powers CV evaluation and job matching.
- **PDF Processing**: Uses `pdfplumber` for text extraction.
- **File Storage**: Stores PDFs in the `inputs` folder.
- **Frontend**: HTML templates with basic CSS styling.

Key files:
- `app.py`: Main Flask application.
- `modules/`: Contains logic for CV evaluation, job matching, and PDF handling.
- `templates/`: HTML files for the user interface.

## Prerequisites
- **Python 3.9+**
- **Docker**
- **Gemini API Key** (from Google Cloud)
- **Dependencies**: Listed in `requirements.txt` (Flask, pdfplumber, google-generativeai).

## Installation
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Jeton-CV-Eval-Engine
   ```

2. **Set Up Virtual Environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Set Gemini API Key**:
   - Create a `.env` file or set:
     ```bash
     export GEMINI_API_KEY='your-api-key-here'
     ```

5. **Run Locally**:
   ```bash
   python app.py
   ```
   Access at `http://localhost:5000`.

## Usage
1. **Upload CVs**:
   - Go to `/`, drag and drop or browse for PDF CVs.
   - Only PDFs are accepted.

2. **View CVs**:
   - Visit `/cv_files` to list and delete CVs or evaluate one.

3. **Evaluate CV**:
   - Go to `/cv_eval/<filename>` for detailed results.

4. **Dream Team**:
   - On `/cv_files`, enter a job description and submit for ranked candidates.

## Project Structure
```
Jeton-CV-Eval-Engine/
├── .cadence
├── .venv
├── inputs/              # Stores uploaded PDFs
├── modules/
│   ├── cv_evaluation_gemini.py  # CV analysis
│   ├── dream_team_evaluator.py  # Job matching
│   ├── pdf_to_text.py          # PDF text extraction
│   ├── pdf_upload.py           # File upload handling
├── static/
│   ├── loader.css
│   ├── style.css
├── templates/
│   ├── cv_eval.html
│   ├── cv_files.html
│   ├── dream.html
│   ├── index.html
├── test/
├── .dockerignore
├── app.py               # Main application
├── Dockerfile
├── README.md
├── requirements.txt
```

## API Integration
Uses Gemini API (`gemini-2.5-pro`) for:
- CV evaluation (candidate details and scores).
- Job matching (match score and reasoning).
Ensure the API key is set and valid.

## Docker Deployment
1. **Build Image**:
   ```bash
   docker build -t cv-evaluation-engine .
   ```

2. **Run Container**:
   ```bash
   docker run -p 5000:5000 -e GEMINI_API_KEY='your-api-key-here' cv-evaluation-engine
   ```
   Access at `http://localhost:5000`.

## Troubleshooting
- **API Errors**: Check `GEMINI_API_KEY` and API quotas.
- **PDF Issues**: Ensure `pdfplumber` is installed and PDFs are valid.
- **File Upload**: Verify `inputs` folder permissions.
- **Docker**: Ensure port 5000 is free.

## Contributing
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push and open a PR.

## License
MIT License. See `LICENSE` for details.

