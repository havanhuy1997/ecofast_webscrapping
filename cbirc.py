from utils import get_json, get_soup, create_soup_from_html_str
from file import save_txt_file

PAGE_SIZE = 18
HOME_URL = 'http://www.cbirc.gov.cn'
URL_FORMAT = 'http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectDocByItemIdAndChild/data_itemId={},pageIndex={},pageSize=' + str(PAGE_SIZE) + '.json'
URL_FORMAT_FOR_ITEMID_916 = 'http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectItemAndDocByItemPId/data_itemId=916,pageSize=3.json'
DETAIL_URL_FORMAT = 'http://www.cbirc.gov.cn/cn/view/pages/ItemDetail.html?docId={}&itemId={}&generaltype=0'
GET_DOC_URL_FORMAT = 'http://www.cbirc.gov.cn/cn/static/data/DocInfo/SelectByDocId/data_docId={}.json'

def get_total_page(total_result):
    print('total_result=', total_result)
    if total_result % PAGE_SIZE == 0:
        return total_result // PAGE_SIZE
    else:
        return total_result // PAGE_SIZE + 1

def get_date_for_tile(date_str):
    date_str = date_str.split()[0]
    date_split = date_str.split('-')
    return date_split[0][-2:] + date_split[1] + date_split[2]

def get_content_of_detail_link(j):
    content_html = j['data']['docClob']
    s = create_soup_from_html_str(content_html)
    p_tags = s.select('.Section0 p')
    return '\n'.join([p_tag.text for p_tag in p_tags])

def check_filter(j, item_pid, item_url, item_name):
    for item in j['data']['listTwoItem']:
        for item_lvs in item['ItemLvs']:
            if item_pid == item_lvs['itemPid'] and item_url == item_lvs['itemUrl'] and item_name == item_lvs['itemName']:
                return True
    return False

def save_rows(rows):
    for row in rows:
        doc_id = row['docId']
        title = row['docTitle']
        publishDate = row['publishDate']
        date_for_title = get_date_for_tile(publishDate)
        link = DETAIL_URL_FORMAT.format(doc_id, data_item_id)
        j = get_json(GET_DOC_URL_FORMAT.format(doc_id))
        save_txt_file(
            'CN/{}_CN_CBIRC'.format(date_for_title),
            publishDate,
            title,
            link,
            get_content_of_detail_link(j),
            remove_non_latin_from_title=False
        )

data_item_ids = [915, 916]

for data_item_id in data_item_ids:
    rows = []
    if data_item_id == 915:
        j = get_json(URL_FORMAT.format(data_item_id, 1))
        total_page = get_total_page(j['data']['total'])
        for page in range(total_page):
            print('Getting results for page:', page)
            search_url = URL_FORMAT.format(data_item_id, page + 1)
            if 'data' in j and 'rows' in j['data']:
                save_rows(j['data']['rows'])
    elif data_item_id == 916:
        j = get_json(URL_FORMAT_FOR_ITEMID_916)
        save_rows(j['data'][0]['docInfoVOList'])