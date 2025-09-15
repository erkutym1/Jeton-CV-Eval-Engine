import os
from werkzeug.utils import secure_filename
from docx2pdf import convert

# The path to the folder where processed files will be saved.
UPLOAD_FOLDER = 'inputs'
# Define the file extensions that the application will accept.
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx'}


def process_and_save_file(file):
    """
    Handles uploaded files. It saves PDFs directly and converts DOC/DOCX files
    to PDF format before saving them in the 'inputs' folder.

    Returns the final PDF filename upon success, otherwise returns None.
    """

    if not file or file.filename == '':
        return None

    # Sanitize the original filename to remove unsafe characters.
    original_filename = secure_filename(file.filename)
    # Split the filename into its base and extension.
    filename_base, extension = os.path.splitext(original_filename)

    # Check if the file's extension is in our allowed list.
    if extension.lower() not in ALLOWED_EXTENSIONS:
        print(f"Unsupported file type: {extension}")
        return None

    # Ensure the target 'inputs' directory exists.
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # Define the final path for the output PDF file.
    final_pdf_path = os.path.join(UPLOAD_FOLDER, f"{filename_base}.pdf")

    try:
        if extension.lower() == '.pdf':
            # If the file is already a PDF, save it directly.
            file.save(final_pdf_path)
            print(f"PDF file saved directly: {final_pdf_path}")

        elif extension.lower() in ['.doc', '.docx']:
            # If the file is a Word document, it needs conversion.
            # First, save the original Word file to a temporary location.
            temp_doc_path = os.path.join(UPLOAD_FOLDER, original_filename)
            file.save(temp_doc_path)
            print(f"Temporary Word document saved: {temp_doc_path}")

            # Convert the temporary Word document to PDF.
            print(f"Converting {temp_doc_path} to {final_pdf_path}...")
            convert(temp_doc_path, final_pdf_path)
            print("Conversion successful.")

            # Remove the temporary Word document after conversion.
            os.remove(temp_doc_path)
            print(f"Temporary file removed: {temp_doc_path}")

        # Return the name of the new PDF file so the app can use it.
        return f"{filename_base}.pdf"

    except Exception as e:
        print(f"An error occurred during file processing: {e}")
        # Clean up any temporary files if an error occurs during conversion.
        if 'temp_doc_path' in locals() and os.path.exists(temp_doc_path):
            os.remove(temp_doc_path)
        return None


def list_uploaded_files():
    """
    Lists all PDF files currently in the 'inputs' folder.
    This ensures the rest of the application only sees the final PDF files.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        return []

    # Filter the list to only include files ending with .pdf.
    files = [f for f in os.listdir(UPLOAD_FOLDER) if f.lower().endswith('.pdf')]
    return files