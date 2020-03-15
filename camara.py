from utils import get_json_with_post, get_total_page
from file import save_txt_file, get_pdf_from_link
import re

SEARCH_URL = 'https://www.camara.leg.br/api/v1/busca/proposicoes/_search'
PDF_LINK_URL = 'https://www.camara.leg.br/proposicoesWeb/prop_mostrarintegra?codteor={}&filename={}'
NUMBER_RESULT_PER_PAGE = 20
json_body = {'order': 'data', 'pagina': 1, 'q': '*'}

def get_json_response():
    return get_json_with_post(SEARCH_URL, json_body)

def get_title_for_file(date_str):
    date_str = date_str.split('T')[0]
    date_split = date_str.split('-')
    return date_split[0][-2:] + date_split[1] + date_split[2]

j = get_json_response()
total_page = get_total_page(j['hits']['total'], NUMBER_RESULT_PER_PAGE)

for page in range(1, total_page + 1):
    json_body['pagina'] = page
    j = get_json_response()
    for hit in j['hits']['hits']:
        source = hit['_source']
        title = source['titulo']
        date = source['dataOrdenacao']
        pdf_file_url = PDF_LINK_URL.format(source['codArquivoTeor'], re.sub('\s+', '+', title))
        save_txt_file(
            'BR/{}_BR_CAMARA'.format(get_title_for_file(date)),
            date,
            title,
            pdf_file_url,
            get_pdf_from_link(pdf_file_url)
        )
