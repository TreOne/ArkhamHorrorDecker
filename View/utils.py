from func import *


def update_all_card_data() -> None:
    """Функция получает обновленную базу карт с сайта ArkhamDB.com
    и обновляет локальную версию"""

    url = 'https://arkhamdb.com/api/public/cards/'
    cards_info = requests.get(url)
    json_bytes = cards_info.content
    json_string = json_bytes.decode()
    remote_base = json.loads(json_string)

    local_base = get_local_base()

    formatted_card_data = {}
    for card in remote_base:
        card_id = card['code']
        if card_id in local_base:
            card.update({'name_rus': local_base[card_id]['name_rus'],
                         'name_pnp': local_base[card_id]['name_pnp'],
                         'name_yndx': local_base[card_id]['name_yndx']})
        else:
            card.update({'name_rus': '',
                         'name_pnp': '',
                         'name_yndx': ''})
        formatted_card_data[card['code']] = card
    with open('db/cards_data.json', 'w+', encoding='utf8') as cards_data_base:
        json.dump(formatted_card_data, cards_data_base, ensure_ascii=False, sort_keys=True, indent=4)


def download_all_card_img() -> None:
    """Скачивает все изображения карт из базы"""
    local_base = get_local_base()
    for card in local_base.values():
        if 'imagesrc' not in card.keys():
            continue
        image_src = card['imagesrc']
        file_extension = os.path.splitext(image_src)[1]
        file_path = 'db/card_images/{}{}'.format(card['code'], file_extension)
        if not os.path.exists(file_path):
            url = 'https://arkhamdb.com{}'.format(image_src)
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, 'wb') as f:
                    f.write(response.content)


def check_card_data():
    """Проверка на совпадения ID карт и URL их изображений"""
    local_base = get_local_base()
    for card in local_base.values():
        if 'imagesrc' not in card.keys():
            continue
        url = card['imagesrc']
        file_extension = os.path.splitext(url)[1]
        url2 = '/bundles/cards/{}{}'.format(card['code'], file_extension)
        if url != url2:
            print('ERROR: "{}" != "{}"'.format(url, url2))
