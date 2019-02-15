import View.res_rc
from PyQt5.QtWidgets import QLabel, QTreeWidget, QTreeWidgetItem
from View.MainWindow import Ui_MainWindow
from PyQt5.QtGui import QPixmap, QIcon, QColor
import requests
import os.path
import json
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen, quote
import re
from time import sleep


def get_card_data(card_id: str) -> json:
    """Получение информации о конкретной карте"""
    local_cards_base = get_local_base()
    if card_id in local_cards_base:
        return local_cards_base[card_id]
    else:
        return None


def get_local_base() -> json:
    """Получение локальной базы карт"""
    with open('db/cards_data.json', 'r', encoding='utf8') as cards_data_json:
        try:
            local_cards_data = json.load(cards_data_json)
        except json.decoder.JSONDecodeError:
            return {}
    return local_cards_data


def show_card_img(ui: QLabel, card_id: str) -> None:
    """Отобразить карту в интерфейсе приложения"""
    card_data = get_card_data(card_id)
    if 'imagesrc' not in card_data.keys():
        ui.setPixmap(QPixmap(":/img/player-card-back.png"))
        return
    image_src = card_data['imagesrc']
    file_extension = os.path.splitext(image_src)[1]
    file_path = 'db/card_images/{}{}'.format(card_id, file_extension)
    if not os.path.exists(file_path):
        print('Скачиваю изображение карты: {}'.format(get_card_data(card_id)['name']))
        url = 'https://arkhamdb.com{}'.format(image_src)
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
    ui.setPixmap(QPixmap(file_path))


def get_html_from_url(url: str) -> 'HTML page':
    # Получаем HTML страницу
    response = urlopen(url)
    # response = urlopen('https://arkhamdb.com/decklist/view/6486/lola-for-cowards-hard-expert-1.0')
    return response.read().decode('utf-8', 'ignore')


def get_deck_info_from_html(html: str) -> 'JSON data':
    # Разбираем полученный HTML (Вытягиваем JS и из него тащим JSON объект с картами)
    parsed_html = BeautifulSoup(html, features="lxml")
    js_on_page = parsed_html.findAll('script', type='text/javascript')
    deck_init_script = js_on_page[-1].string
    deck_data_pattern = re.compile('app.deck.init\((.*?)\);\n\sapp.user.params.decklist_id')
    cards_list = deck_data_pattern.findall(deck_init_script).pop(0)
    deck_data = json.loads(cards_list)
    return deck_data


def setup_empty_tree(deck_viewer: QTreeWidget):
    """Setup empty Tree at startup. """
    deck_viewer.setColumnCount(2)
    deck_viewer.setColumnWidth(0, 70)
    deck_viewer.setHeaderHidden(True)


def add_tree_root(tw: QTreeWidget, name: str):
    item = QTreeWidgetItem(tw)
    item.setExpanded(True)
    item.setText(0, name)
    item.setFirstColumnSpanned(True)
    return item


def add_tree_child(parent: QTreeWidgetItem, name: str, faction_code: str, count: int):
    item = QTreeWidgetItem()
    if count > 1:
        item.setText(0, 'x{}'.format(count))
    item.setText(1, name)
    item.setForeground(1, get_faction_color(faction_code))
    file_icon = QIcon(':/icon/{}.png'.format(faction_code))
    item.setIcon(1, file_icon)
    parent.addChild(item)
    return item


def get_faction_color(faction_code: str) -> QColor:
    faction_colors = dict(neutral=QColor(96, 96, 96),
                          guardian=QColor(43, 128, 197),
                          seeker=QColor(236, 132, 38),
                          rogue=QColor(16, 113, 22),
                          mystic=QColor(67, 49, 185),
                          survivor=QColor(204, 48, 56))
    return faction_colors.get(faction_code, QColor(96, 96, 96))


def clear_deck_viewer(ui: Ui_MainWindow) -> None:
    ui.deck_viewer.clear()
    ui.card_face.setPixmap(QPixmap(":/img/player-card-back.png"))


def translate_en_ru(text):
    """Запрос перевода с сайта Яндекс.Переводчик"""
    api_key = 'trnsl.1.1.20180809T082714Z.5ba6c8b414e5a3cc.03244ad6c99c3971ed6cae6ff2eb69bf7a9bcc72'
    base = 'https://translate.yandex.net'
    post = '/api/v1.5/tr.json/translate?key=' + api_key + '&text=' + quote(text) + '&lang=en-ru'
    url = base+post

    q = Request(url)
    q.add_header('accept', 'json')
    a = urlopen(q).read().decode('utf-8', 'ignore')
    answer = json.loads(a)
    translated_text = answer['text'].pop()
    sleep(1)
    return translated_text


def save_new_card_data(eng_name, rus_name, pnp_name):
    local_cards_base = get_local_base()
    for card in local_cards_base.values():
        if eng_name == card['name']:
            if rus_name != "":
                card['name_rus'] = rus_name
            if pnp_name != "":
                card['name_pnp'] = pnp_name

    with open('db/cards_data.json', 'w+', encoding='utf8') as cards_data_base:
        json.dump(local_cards_base, cards_data_base, ensure_ascii=False, sort_keys=True, indent=4)
