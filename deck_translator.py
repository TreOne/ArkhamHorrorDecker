import sys
from collections import Counter, OrderedDict
from pprint import pprint
from View.MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from func import *

top_cards = Counter({'01000': 235, '01088': 217, '01093': 206, '01089': 185, '01090': 147, '01087': 146, '01091': 138,
                     '01092': 132, '01020': 101, '01025': 100, '01080': 90, '01065': 89, '01060': 84, '01030': 82,
                     '01050': 80, '01064': 77, '01039': 70, '02022': 69, '01048': 64, '02032': 63, '01059': 62,
                     '01033': 61, '01018': 61, '01086': 61, '01023': 61, '01079': 60, '01016': 59, '01051': 55,
                     '02188': 55, '01072': 54, '01022': 54, '01037': 48, '02111': 47, '02028': 44, '02033': 44,
                     '01073': 43, '02184': 41, '01021': 40, '01017': 39, '02117': 38, '01075': 38, '01063': 38,
                     '01024': 38, '02026': 38, '01036': 37, '01067': 37, '01045': 36, '01062': 35, '01049': 34,
                     '01058': 33, '02234': 32, '01052': 32, '01019': 31, '02025': 31, '02227': 31, '01047': 31,
                     '01066': 30, '01031': 30, '03158': 30, '03039': 29, '01061': 29, '02014': 28, '01046': 28,
                     '02229': 28, '02015': 28, '01007': 27, '01006': 27, '01034': 26, '02272': 25, '02011': 25,
                     '02010': 25, '02149': 25, '03033': 24, '01014': 24, '01015': 24, '02020': 23, '02116': 23,
                     '01032': 22, '01074': 22, '02006': 22, '01013': 22, '02007': 22, '01012': 22, '02024': 21,
                     '02158': 21, '02107': 20, '01009': 20, '01035': 20, '01008': 20, '03231': 18, '02009': 18,
                     '03155': 18, '02017': 18, '02008': 18, '03198': 17, '02151': 17, '03191': 17, '02105': 17,
                     '02012': 16, '02013': 16, '03026': 16, '02021': 16, '01076': 15, '01081': 15, '03029': 15,
                     '03233': 15, '02225': 15, '03114': 15, '02186': 15, '03153': 14, '02302': 14, '02232': 14,
                     '03117': 14, '01038': 13, '01053': 13, '03020': 13, '03112': 13, '03269': 13, '01077': 13,
                     '01010': 13, '01011': 13, '02029': 13, '03012': 12, '03267': 12, '03013': 12, '02023': 12,
                     '02110': 12, '01044': 11, '03116': 11, '03037': 11, '03118': 11, '02192': 10, '04010': 10,
                     '04011': 10, '04037': 10, '02189': 10, '03024': 10, '04012': 10, '03022': 10, '01097': 10,
                     '03031': 10, '03196': 10})

card_list = list(top_cards.most_common())


def load_deck() -> json:
    data_for_treeview = {}
    for card_id, count in card_list:
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


#pprint(load_deck())


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
    deck = load_deck()
    sorted_deck = OrderedDict(sorted(deck.items()))
    for card_type in sorted_deck:
        parent = add_tree_root(ui.deck_viewer, card_type.title())
        for card in deck[card_type]:
            add_tree_child(parent, **card)


def save_new_card():
    save_new_card_data(ui.card_name_eng.text(), ui.card_name_rus.text(), ui.card_name_pnp.text())


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
# Для отладки автоматически вводится адрес тестовой страницы
ui.deck_url.setText('Выбирать колоду не нужно. Карты загружаются автоматически.')
load_test_data()
ui.save_changes.clicked.connect(save_new_card)
ui.deck_viewer.itemClicked.connect(show_card)
setup_empty_tree(ui.deck_viewer)
MainWindow.show()
sys.exit(app.exec_())
