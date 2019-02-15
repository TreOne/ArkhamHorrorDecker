import sys
from pprint import pprint

from View.MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtCore import QModelIndex
from func import *


def load_deck() -> json:
    url = ui.deck_url.text()
    deck_page_html = get_html_from_url(url)
    deck_info = get_deck_info_from_html(deck_page_html)
    data_for_treeview = {}
    for card_id, count in deck_info['slots'].items():
        card_data = get_card_data(card_id)
        type_code = card_data.get('type_code', 'Other')
        if type_code not in data_for_treeview:
            data_for_treeview[type_code] = []
        eng_name = card_data.get('name', 'None')
        name_pnp = card_data.get('name_pnp', '')
        name_rus = card_data.get('name_rus', '')
        if name_rus != '':
            name = name_rus
        elif name_pnp != '':
            name = name_pnp
        else:
            name = eng_name
        data_for_treeview[type_code].append({'name': name,
                                             'faction_code': card_data.get('faction_code', 'neutral'),
                                             'count': count})
    return data_for_treeview


def show_card(self):
    card = find_card_from_name(self.text(1))
    if card['code'] == '01000':
        ui.card_face.setPixmap(QPixmap(":/img/player-card-back.png"))
    else:
        show_card_img(ui.card_face, card['code'])
    ui.card_name_eng.setText(card['name'])
    ui.card_name_rus.setText(card['name_rus'])
    ui.card_name_pnp.setText(card['name_pnp'])
    if card['name_yndx'] == '':
        translated_name = translate_en_ru(card['name'])
        ui.card_name_translated.setText(translated_name)
        local_cards_base = get_local_base()
        for card1 in local_cards_base.values():
            if card['name'] == card1['name']:
                if translated_name != "":
                    card1['name_yndx'] = translated_name

        with open('db/cards_data.json', 'w+', encoding='utf8') as cards_data_base:
            json.dump(local_cards_base, cards_data_base, ensure_ascii=False, sort_keys=True, indent=4)
    else:
        ui.card_name_translated.setText(card['name_yndx'])
    # print(dir(self.icon(1).name()))
    # item.setForeground(1, get_faction_color('neutral'))
    # print(item.icon())


def find_card_from_name(card_name: str) -> json:
    local_cards_base = get_local_base()
    for card in local_cards_base.values():
        if card_name == card['name']:
            return card
        if card_name == card['name_pnp']:
            return card
        if card_name == card['name_rus']:
            return card
    return None


def load_test_data():
    clear_deck_viewer(ui)
    for card_type, list_cards_of_this_type in load_deck().items():
        parent = add_tree_root(ui.deck_viewer, card_type.title())
        for card in list_cards_of_this_type:
            add_tree_child(parent, **card)


def save_new_card():
    save_new_card_data(ui.card_name_eng.text(), ui.card_name_rus.text(), ui.card_name_pnp.text())


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
# Для отладки автоматически вводится адрес тестовой страницы
ui.deck_url.setText('https://arkhamdb.com/decklist/view/6486/lola-for-cowards-hard-expert-1.0')
ui.load_deck_btn.clicked.connect(load_test_data)
ui.save_changes.clicked.connect(save_new_card)
ui.deck_viewer.itemClicked.connect(show_card)
setup_empty_tree(ui.deck_viewer)
MainWindow.show()
sys.exit(app.exec_())
