import os
import requests
from io import BytesIO
import PyPDF2
import slate3k as slate
from config import OUTPUT_DIR
import re

def create_folder_if_not_existing(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

create_folder_if_not_existing(OUTPUT_DIR)

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

def save_txt_file(folder_name, date, title, href, content, remove_non_latin_from_title=True):
    output_dir = OUTPUT_DIR + folder_name
    create_folder_if_not_existing(output_dir)
    if remove_non_latin_from_title:
        title_file_name = re.sub('[^0-9a-zA-Z]', '', title)
    else:
        title_file_name = title
    file_name = '{}_{}.txt'.format(folder_name.split('/')[-1], title_file_name)
    with open(output_dir + '/' + file_name, 'w', encoding="utf-8") as f:
        print('+ Saving {}-{}'.format(title, date))
        f.write(date + '\n')
        f.write(title + '\n')
        f.write(href + '\n')
        if type(content) == str:
            f.write(content)
        else:
            f.writelines(content)