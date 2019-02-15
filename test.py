from PyQt5.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QHBoxLayout, QWidget
from PyQt5.QtGui import QFont
from bs4 import BeautifulSoup
import sys
from func import *
from PIL import Image
from os.path import basename
import markdown2


class Ui_MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.html_viewer = QTextEdit()
        self.html_viewer.setMinimumSize(600, 370)
        self.html_viewer.setMaximumSize(600, 16777215)
        self.html_viewer.setFont(QFont('Open Sans', 10, weight=QFont.Normal))

        vbox = QVBoxLayout()
        vbox.addWidget(self.html_viewer)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.resize(620, 800)
        self.setMinimumSize(620, 400)
        self.setMaximumSize(620, 16777215)
        self.setWindowTitle('Редактор гайдов')
        self.show()


def load_description() -> 'HTML':
    url = 'https://arkhamdb.com/decklist/view/2381'

    #print(dir(markdown))

    deck_page_html = get_html_from_url(url)
    deck_info = get_deck_info_from_html(deck_page_html)
    description_markdown = deck_info['description_md']

    investigator_name = deck_info['investigator_name']
    deck_id = deck_info['id']
    local_file_path = create_local_folder(investigator_name, deck_id)
    description_markdown_clear = save_and_clear_md_guide(description_markdown, local_file_path)
    deck_description = markdown_to_html(description_markdown_clear)

    parsed_html = BeautifulSoup(deck_description, features="lxml")
    image_fix(parsed_html, local_file_path)
    save_guide(parsed_html, local_file_path)
    html = open_guide(local_file_path)

    string_html = str(html)
    #card_insert_pattern = re.compile('\[([^\]]*)\]\(/card/([^\)]*)\)')
    #result_html = re.sub(card_insert_pattern, insert_card_to_guide, string_html)
    #result_html = markdown.markdown(result_html)
    ui.html_viewer.setHtml(string_html)
    #print(result_html)


def image_fix(html: BeautifulSoup, local_file_path) -> str:
    tags = html.findAll('h1')
    for tag in tags:
        wrapper = html.new_tag('p')
        tag.wrap(wrapper)

    images = html.findAll('img')

    # Обернуть все картинки в тег <p>. Сохранить все уникальные адреса картинок.
    image_sources = set()
    for image in images:
        image_sources.add(image['src'])
        wrapper = html.new_tag('p')
        image.wrap(wrapper)

    # Скачивание нужных картинок из гайда и маштабирование по размеру
    max_img_width = 555
    for image_src in image_sources:
        image_name = get_filename_from_filepath(image_src)
        image_filepath = local_file_path + image_name
        if not os.path.exists(image_filepath):
            response = requests.get(image_src)
            if response.status_code == 200:
                with open(image_filepath, 'wb') as f:
                    f.write(response.content)
                original_image = Image.open(image_filepath)
                w, h = original_image.size
                if w > max_img_width:
                    original_image.thumbnail((max_img_width, h), Image.ANTIALIAS)
                    original_image.save(image_filepath)
    for image in images:
        file_name = os.path.split(image['src'])[1]
        full_path = file_name
        image['src'] = full_path

    return html


def save_and_clear_md_guide(description_markdown: str, local_file_path: str) -> str:
    description_markdown = description_markdown.replace('\r', '')
    img_tag_pattern = re.compile('(<img\s[^>]*>)')
    description_markdown = re.sub(img_tag_pattern, r'\n\1\n', description_markdown)
    guide_file_patch = local_file_path + "guide_md.html"
    with open(guide_file_patch, "w", encoding='utf8') as file:
        file.write(description_markdown)
    with open(guide_file_patch, 'r', encoding='utf8') as file:
        description_markdown_clear = file.read()
    return description_markdown_clear


def save_guide(parsed_html: BeautifulSoup, local_file_path: str):
    guide_file_patch = local_file_path + "guide.html"
    with open(guide_file_patch, "w", encoding='utf8') as file:
        file.write(parsed_html.prettify())


def open_guide(local_file_path: str) -> str:
    guide_file_patch = local_file_path + "guide.html"
    with open(guide_file_patch, 'r', encoding='utf8') as guide_file:
        html = BeautifulSoup(guide_file, features="lxml")
    images = html.findAll('img')
    for image in images:
        file_name = os.path.split(image['src'])[1]
        full_path = local_file_path + file_name
        image['src'] = full_path
    return html


def create_local_folder(investigator_name: str, deck_id: str) -> str:
    local_file_path = 'db/decklist/{}/{}/'.format(investigator_name, deck_id)
    if not os.path.exists(local_file_path):
        os.makedirs(local_file_path)
    return local_file_path


def get_filename_from_filepath(filepath: str) -> str:
    file_name_with_request = os.path.split(filepath)[1]
    deck_data_pattern = re.compile('([^?]*)(\?)?')
    file_name = deck_data_pattern.findall(file_name_with_request).pop(0)
    file_name = file_name[0]
    return file_name


def markdown_to_html(md_code: str) -> str:
    html = markdown2.markdown(md_code)
    return html


def insert_card_to_guide(match_obj):
    # r'<a href="/card/\2" data-hasqtip="1" aria-describedby="qtip-1">\1</a>'
    card_id = match_obj.group(2)
    card_name = match_obj.group(1)
    card = get_card_data(card_id)
    if card is not None and card['name_pnp'] != '':
        card_name = card['name_pnp']
    return r'<a href="/card/{}" data-hasqtip="1" aria-describedby="qtip-1">{}</a>'.format(
        card_id,
        card_name)


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Ui_MainWindow()
    load_description()
    sys.exit(app.exec_())
