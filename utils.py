import requests
from bs4 import BeautifulSoup
import json

def get_soup(url):
    r = requests.get(url)
    return BeautifulSoup(r.content, features='lxml')

def get_json(url):
    r = requests.get(url)
    return json.loads(r.content)

def create_soup_from_html_str(html_str):
    return BeautifulSoup(html_str, features='lxml')