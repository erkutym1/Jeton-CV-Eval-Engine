# modules/pdf_to_text.py

import pdfplumber
import os

# Yüklenen dosyaların bulunduğu klasör
INPUTS_FOLDER = 'inputs'


def extract_text_from_pdf(filename):
    """
    Belirtilen PDF dosyasının metin içeriğini çıkarır.

    Args:
        filename (str): 'inputs' klasöründeki PDF dosyasının adı.

    Returns:
        str: PDF'in tüm metin içeriği. Dosya bulunamazsa veya bir hata oluşursa
             bir hata mesajı döndürür.
    """
    filepath = os.path.join(INPUTS_FOLDER, filename)

    if not os.path.exists(filepath):
        return f"Hata: '{filename}' adında bir dosya bulunamadı."

    try:
        full_text = ""
        # pdfplumber ile PDF dosyasını aç
        with pdfplumber.open(filepath) as pdf:
            # PDF'in her bir sayfasını döngüye al
            for page in pdf.pages:
                # Sayfadaki metni çıkar ve mevcut metne ekle
                # extract_text() None döndürürse boş string ekle
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + "\n\n"  # Sayfalar arasına boşluk koy

        return full_text
    except Exception as e:
        return f"PDF işlenirken bir hata oluştu: {e}"