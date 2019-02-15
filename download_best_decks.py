import json
from pprint import pprint
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from collections import Counter


def get_html_from_url(url: str) -> 'HTML page':
    # Получаем HTML страницу
    response = urlopen(url)
    # response = urlopen('https://arkhamdb.com/decklist/view/6486/lola-for-cowards-hard-expert-1.0')
    return response.read()


def get_deck_info_from_html(page_html: str) -> 'JSON data':
    # Разбираем полученный HTML (Вытягиваем JS и из него тащим JSON объект с картами)
    parsed_html = BeautifulSoup(page_html, features="lxml")
    js_on_page = parsed_html.findAll('script', type='text/javascript')
    deck_init_script = js_on_page[-1].string
    deck_data_pattern = re.compile('app.deck.init\((.*?)\);\n\sapp.user.params.decklist_id')
    cards_list = deck_data_pattern.findall(deck_init_script).pop(0)
    deck_data = json.loads(cards_list)
    return deck_data


def get_cards_from_deck(deck_data: json) -> set:
    return set(deck_data['slots'])


def get_html_from_page(page_num: int) -> 'HTML page':
    url = 'https://arkhamdb.com/decklists/find/{}?sort=likes'.format(page_num)
    response = urlopen(url)
    return response.read()


def get_top_deck_from_html(page_html: str) -> set:
    parsed_html = BeautifulSoup(page_html, features='lxml')
    decks_html_list = parsed_html.findAll('a', 'decklist-name')
    decks_links = set()
    for deck_html_link in decks_html_list:
        deck_link = 'https://arkhamdb.com{}'.format(deck_html_link['href'])
        decks_links.add(deck_link)
    return decks_links


top_decks = set()
for page in range(1, 11):
    html = get_html_from_page(page)
    top_decks.update(get_top_deck_from_html(html))

top_cards = Counter()

i = 0
for link in top_decks:
    i += 1
    print('Добавляем колоду номер: {}'.format(i))
    deck_html = get_html_from_url(link)
    deck_info = get_deck_info_from_html(deck_html)
    cards_in_deck = get_cards_from_deck(deck_info)
    top_cards.update(cards_in_deck)

print(top_cards)
