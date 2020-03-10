import requests
from bs4 import BeautifulSoup
from file import create_folder_if_not_existing
from config import OUTPUT_DIR
import re

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, features='lxml')

def exist_next_page(soup):
    navigation_a_tags = soup.select('#bottomPageNav .sucheWeiter a')
    if navigation_a_tags and navigation_a_tags[-1].select_one('span').text == 'weiter':
        return True
    return False

def get_soup_of_with_h_and_gtyp(h, gtyp):
    url = filter_url_base.format(h, gtyp)
    return get_soup(url)

filter_url_base = 'https://pdok.bundestag.de/treffer.php?h={}&q=19%2F%2A&gtyp={}'
gtyps = ['Gesetze', 'Verordnungen']
RESULTS_PER_PAGE = 10

create_folder_if_not_existing(OUTPUT_DIR)

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
            full_content = tr.select_one('.fullCont').text
            date = tr.select('.resultText strong')[1].text

            output_dir = OUTPUT_DIR + '{}_DE_BUNDESTAG'.format(date)
            create_folder_if_not_existing(output_dir)
            file_name = '{}_DE_BUNDESTAG_{}'.format(date, re.sub('\W', '', title))
            with open(output_dir + '/' + file_name, 'w') as f:
                print('+ Saving {}'.format(title))
                f.write(date + '\n')
                f.write(title + '\n')
                f.write(href + '\n')
                f.write(full_content)
        if exist_next_page(soup):
            h += RESULTS_PER_PAGE
        else:
            break