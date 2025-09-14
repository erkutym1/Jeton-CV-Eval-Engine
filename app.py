from flask import Flask, render_template, request, redirect, url_for, flash
from modules.pdf_upload import save_pdf, list_uploaded_files
from modules.pdf_to_text import extract_text_from_pdf
from modules.cv_evaluator import evaluate_cv_with_llama

app = Flask(__name__)
app.secret_key = 'a_very_secret_key'


# ... (routes for '/', '/upload', and '/cv_files' remain exactly the same) ...
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected!')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No file selected!')
        return redirect(url_for('index'))
    if file and file.filename.endswith('.pdf'):
        save_pdf(file)
        return redirect(url_for('cv_files'))
    else:
        flash('Please upload a PDF file only!')
        return redirect(url_for('index'))


@app.route('/cv_files')
def cv_files():
    uploaded_files = list_uploaded_files()
    return render_template('cv_files.html', files=uploaded_files)


@app.route('/cv_eval/<filename>')
def evaluate_cv(filename):
    # Step 1: Extract text from the CV
    extracted_text = extract_text_from_pdf(filename)

    # Step 2: Send the extracted text to our LOCAL Llama 3 for evaluation
    # UPDATED FUNCTION CALL
    evaluation_results = evaluate_cv_with_llama(extracted_text)

    # Step 3: Send raw text and evaluation results to the template
    return render_template(
        'cv_eval.html',
        filename=filename,
        extracted_text=extracted_text,
        evaluation_results=evaluation_results
    )


if __name__ == '__main__':
    app.run(debug=True)