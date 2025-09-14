import os
from werkzeug.utils import secure_filename

# Yüklenen dosyaların kaydedileceği klasörün yolu
# Bu yol, app.py'nin bulunduğu ana dizine göre belirlenir.
UPLOAD_FOLDER = 'inputs'


def save_pdf(file):
    """
    Yüklenen PDF dosyasını 'inputs' klasörüne kaydeder.
    Güvenlik için dosya adını temizler.
    """
    if file and file.filename != '':
        # Dosya adını güvenlik zafiyetlerine karşı temizle (örn: ../../)
        filename = secure_filename(file.filename)

        # 'inputs' klasörünün var olup olmadığını kontrol et, yoksa oluştur
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        # Dosyayı kaydetmek için tam yolu oluştur
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        print(f"Dosya başarıyla kaydedildi: {filepath}")
        return filename
    return None


def list_uploaded_files():
    """
    'inputs' klasöründeki tüm dosyaları listeler.
    """
    if not os.path.exists(UPLOAD_FOLDER):
        return []

    files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
    return files