import os
import requests
from io import BytesIO
import PyPDF2
import slate3k as slate

def create_folder_if_not_existing(folder_path):
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

def get_pdf_from_link(link):
    print('Getting pdf content:', link)
    content = ''
    r = requests.get(link)
    file_bytes = BytesIO(r.content)
    pdf_reader = PyPDF2.PdfFileReader(file_bytes)
    for i in range(pdf_reader.getNumPages()):
        try:
            page = pdf_reader.getPage(i)
            text = page.extractText()
            if i == 0 and text.strip() and ' ' not in text:
                break
            content += page.extractText()
        except Exception as e:
            print('Error {} when getting content for page: {}'.format(str(e), i))
    if not content:
        file_bytes = BytesIO(r.content)
        content = slate.PDF(file_bytes)
    return content