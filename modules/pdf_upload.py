import os
from werkzeug.utils import secure_filename

# The path to the folder where uploaded files will be saved.
# This path is relative to the main directory where app.py is located.
UPLOAD_FOLDER = 'inputs'

def save_pdf(file):
    """
    Saves the uploaded PDF file to the 'inputs' folder.
    Cleans the filename for security purposes.
    """
    if file and file.filename != '':
        # Sanitize the filename to prevent security vulnerabilities (e.g., directory traversal attacks).
        filename = secure_filename(file.filename)

        # Check if the 'inputs' folder exists; if not, create it.
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Create the full path to save the file.
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"File saved successfully: {filepath}")
        return filename
    return None

def list_uploaded_files():
    """
    Lists all files currently in the 'inputs' folder.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        return []

    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return files