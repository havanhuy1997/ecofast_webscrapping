import requests
from bs4 import BeautifulSoup
import json

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, features='lxml')

def get_json(url):
    r = requests.get(url)
    return json.loads(r.content)

def get_json_with_post(url, json_body):
    r = requests.post(url, json=json_body)
    return json.loads(r.content)

def create_soup_from_html_str(html_str):
    return BeautifulSoup(html_str, features='lxml')

def get_total_page(total_result, number_result_per_page):
    print('total_result=', total_result)
    if total_result % number_result_per_page == 0:
        return total_result // number_result_per_page
    else:
        return total_result // number_result_per_page + 1