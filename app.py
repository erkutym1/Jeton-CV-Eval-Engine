import os
from flask import Flask, render_template, request, redirect, url_for, flash
from modules.pdf_upload import save_pdf, list_uploaded_files
from modules.pdf_to_text import extract_text_from_pdf
from modules.cv_evaluation_gemini import evaluate_cv_with_gemini
from modules.dream_team_evaluator import get_match_score_for_role

app = Flask(__name__)
app.secret_key = 'a_very_very_too_very_secret_key_is_1234'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected!')
        return redirect(request.url)
    files = request.files.getlist('file')
    if not files or all(file.filename == '' for file in files):
        flash('No file selected!')
        return redirect(url_for('index'))
    valid_files = True
    for file in files:
        if not (file and file.filename.endswith('.pdf')):
            valid_files = False
            flash('Please upload PDF files only!')
            break
    if valid_files:
        for file in files:
            save_pdf(file)
        return redirect(url_for('cv_files'))
    return redirect(url_for('index'))


@app.route('/cv_files')
def cv_files():
    uploaded_files = list_uploaded_files()
    return render_template('cv_files.html', files=uploaded_files)


# NEW: Route for bulk file deletion
@app.route('/delete_files', methods=['POST'])
def delete_files():
    # Get the list of filenames to delete from the form
    files_to_delete = request.form.getlist('files_to_delete')
    for filename in files_to_delete:
        try:
            # Construct the file path and ensure it exists before deleting
            filepath = os.path.join('inputs', filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                flash(f'Successfully deleted {filename}.')
        except Exception as e:
            flash(f'Error deleting {filename}: {e}')
    return redirect(url_for('cv_files'))



#for api evaluation
@app.route('/cv_eval/<filename>')
def evaluate_cv(filename):
    # Bu endpoint artık SADECE temel değerlendirmeyi yapar.
    extracted_text = extract_text_from_pdf(filename)
    evaluation_results = evaluate_cv_with_gemini(extracted_text)

    if 'scores' not in evaluation_results:
        evaluation_results['scores'] = {}

    return render_template(
        'cv_eval.html',
        filename=filename,
        extracted_text=extracted_text,
        evaluation_results=evaluation_results
    )


# --- GÜNCELLEME BU FONKSİYONDA ---
@app.route('/dream_team', methods=['POST'])
def dream_team():
    description = request.form.get('description')
    if not description:
        flash('Project or position description cannot be empty.')
        return redirect(url_for('cv_files'))

    all_files = list_uploaded_files()
    final_candidates = []

    print("\n--- Starting Dream Team Analysis (Separated Logic) ---")
    for filename in all_files:
        print(f"\nProcessing Candidate: {filename}")
        cv_text = extract_text_from_pdf(filename)

        # Adım 1: Her aday için temel değerlendirmeyi al (isim, e-posta, genel puan vb.)
        evaluation = evaluate_cv_with_gemini(cv_text)
        if 'error' in evaluation:
            print(f"  └── Step 1 FAILED: Basic evaluation. Error: {evaluation['error']}")
            continue

        print(f"  └── Step 1 SUCCESS: Basic info for {evaluation.get('candidate_name', 'N/A')}.")

        # Adım 2: Her aday için role özel uygunluk puanını ve gerekçeyi al
        match_details = get_match_score_for_role(cv_text, description)
        if 'error' in match_details:
            print(f"  └── Step 2 FAILED: Match scoring. Error: {match_details['error']}")
            continue

        print(f"  └── Step 2 SUCCESS: Match score is {match_details.get('match_score', 'N/A')}.")

        # Adım 3: İki sonucu birleştirerek nihai profili oluştur
        candidate_profile = {
            'filename': filename,
            'evaluation': evaluation,
            'match_score': match_details.get('match_score', 0),
            'reasoning': match_details.get('reasoning', 'No reasoning provided.')
        }
        final_candidates.append(candidate_profile)

    # Adım 4: Adayları role özel uygunluk puanına göre sırala
    final_candidates.sort(key=lambda x: x.get('match_score', 0), reverse=True)

    print(f"\n--- Analysis Complete: Successfully processed and ranked {len(final_candidates)} candidates. ---")

    return render_template('dream.html', candidates=final_candidates, query=description)




if __name__ == '__main__':
    app.run(debug=True)