# CV Evaluation Engine (with Local Llama 3)

This is a web application designed to evaluate curricula vitae (CVs) of data professionals. To address concerns over **API rate limits, potential costs, and data privacy**, the evaluation process is handled entirely by a locally running **Meta-Llama-3-8B-Instruct** model.

This approach provides a secure, cost-free, and fully offline-capable AI solution that does not share sensitive personal information from CVs with any third-party services.

## ✨ Features

- **PDF Upload:** Easily upload CVs through a web interface.
- **Text Extraction:** Automatically extracts text content from uploaded PDFs.
- **Local AI Evaluation:** Smart analysis and scoring using a local `Llama 3 8B` GGUF model.
- **Data Privacy & Security:** Personal information from CVs is never sent to external services; all processing remains on your local machine.
- **API-Independent:** No need to manage API keys, monthly fees, or rate limits.
- **Structured Output:** The model extracts the following information from the CV in JSON format:
  - Skills Found (`skills_found`)
  - Total Years of Experience (`experience_years`)
  - Highest Education Level (`education_level`)
  - Professional Summary (`summary`)
  - Detailed Scoring (`scores`)
- **Web Interface:** A simple and user-friendly interface to display the evaluation results and the raw text.
- **Docker Support:** Docker configuration to easily run the project in an isolated environment.

## 🛠️ Technology Stack

- **Backend:** Flask
- **AI / LLM:** Llama-cpp-python
- **Model:** Meta-Llama-3-8B-Instruct (in Q4_0.gguf format)
- **PDF Processing:** pdfplumber
- **Frontend:** HTML, CSS
- **Containerization:** Docker

## 📂 Project Structure

```
Jeton-CV-Eval-Engine/
├── model/
│   └── Meta-Llama-3-8B-Instruct.Q4_0.gguf  <-- Place the model file here
├── modules/
│   ├── __init__.py
│   ├── cv_evaluator.py     # Local Llama 3 evaluation logic
│   ├── pdf_to_text.py      # PDF to text extraction
│   └── pdf_upload.py       # File saving logic
├── static/
│   └── ...
├── templates/
│   └── ...
├── app.py                  # Main Flask application
├── Dockerfile              # Instructions for building the Docker image
├── requirements.txt        # Python dependencies
└── README.md
```

## 🚀 Setup and Installation

There are two methods to run this project: **Local Setup** (recommended first step) and **Docker Setup**.

### 1. Local Setup (Recommended)

This method runs the model directly on your machine and offers a faster initial setup.

**Step 1: Clone the Repository**
```bash
git clone <repository_url>
cd Jeton-CV-Eval-Engine
```

**Step 2: Create and Activate a Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
**Warning:** The installation of `llama-cpp-python` may require a C++ compiler on your system and might take some time.
```bash
pip install -r requirements.txt
```

**Step 4: Download and Place the Model**
1.  Create a folder named `model` in the project's root directory.
2.  Download the `Meta-Llama-3-8B-Instruct.Q4_0.gguf` model from a source like [Hugging Face](https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF).
3.  Place the downloaded `.gguf` file inside the `model` folder you created.

**Step 5: Run the Application**
```bash
python app.py
```

**Step 6: Access the Interface**
Open your web browser and navigate to `http://localhost:5000`.

### 2. Docker Setup (Advanced)

This method runs the entire application and its dependencies in an isolated container.

**Prerequisites:**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running on your computer.

**Step 1: Prepare the Model**
Follow **Step 4** from the local setup to prepare the `model` folder and the `.gguf` file within it. The model will be copied into the Docker image.

**Step 2: Build the Docker Image**
**Warning:** This process can be **very slow** as it will compile `llama-cpp-python` and copy the large model file into the image. The resulting image will be **several GBs in size**.
```bash
docker build -t cv-evaluation-engine .
```

**Step 3: Run the Docker Container**
```bash
docker run -d -p 5001:5000 --name cv-engine-container cv-evaluation-engine
```
- `-p 5001:5000`: Maps port 5001 on your host machine to port 5000 in the container.

**Step 4: Access the Interface**
Open your web browser and navigate to `http://localhost:5001`.

1.  Open the application in your browser.
2.  Upload a PDF CV by clicking the "Browse file" button or by using drag-and-drop.
3.  Press the "Submit" button.
4.  On the file list page you are redirected to, click on the name of the file you uploaded.
5.  The evaluation page will open.
    - **Note:** The first evaluation may take some time as the model needs to be loaded into memory. Subsequent evaluations will be faster.