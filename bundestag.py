from file import create_folder_if_not_existing, get_pdf_from_link, save_txt_file
import re
from utils import get_soup

def exist_next_page(soup):
    navigation_a_tags = soup.select('#bottomPageNav .sucheWeiter a')
    if navigation_a_tags and navigation_a_tags[-1].select_one('span').text == 'weiter':
        return True
    return False

def get_soup_of_with_h_and_gtyp(h, gtyp):
    url = filter_url_base.format(h, gtyp)
    return get_soup(url)

def get_date_for_title(date_str):
    date_split = date_str.split('.')
    if len(date_split) > 2:
        return date_split[2][-2:] + date_split[1] + date_split[0]
    return date_str

filter_url_base = 'https://pdok.bundestag.de/treffer.php?h={}&q=19%2F%2A&gtyp={}'
gtyps = ['Gesetze', 'Verordnungen']
RESULTS_PER_PAGE = 10

for gtyp in gtyps:
    h = 0
    while True:
        print('Getting result with h={}'.format(h))
        soup = get_soup_of_with_h_and_gtyp(h, gtyp)
        trs = soup.select('.suchErgebnis tr')
        for tr in trs[1:]:
            a_tag = tr.select_one('.resultTitle a')
            href = a_tag.attrs['href']
            title = a_tag.text
            pdf_doc = get_pdf_from_link(href)
            date = tr.select('.resultText strong')[1].text
            date_for_title = get_date_for_title(date)

            save_txt_file(
                'DE/{}_DE_BUNDESTAG'.format(date_for_title),
                date, 
                title, 
                href, 
                pdf_doc
            )
        if exist_next_page(soup):
            h += RESULTS_PER_PAGE
        else:
            break