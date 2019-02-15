
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QTreeWidget
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFileIconProvider
from PyQt5.QtCore import QFileInfo
import View.res_rc

print(dir(QTreeWidgetItem))

class Form(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)
        self.setWindowTitle("QTreeWidget Column")
        self.setFixedWidth(600)
        self.setFixedHeight(400)

        # 데이터
        data = [
            {"type": "В руку",
             "objects": [("Apple", "Red"), ("Banana", "Yellow")]},
            {"type": "Союзники",
             "objects": [("Carrot", "Red"), ("Tomato", "Red")]},
        ]
        # QTreeView 생성 및 설정
        self.tw = QTreeWidget(self)
        self.tw.setColumnCount(2)
        self.tw.setColumnWidth(0, 60)
        # self.tw.setHeaderLabels(["Кол-во", "Название"])
        self.tw.setHeaderHidden(True)
        self.tw.setFixedWidth(600)
        self.tw.setFixedHeight(400)

        for d in data:
            parent = self.add_tree_root(d['type'], "")
            for child in d['objects']:
                self.add_tree_child(parent, *child)

    def add_tree_root(self, name:str, description:str):
        item = QTreeWidgetItem(self.tw)
        item.setExpanded(True)
        item.setText(0, name)
        item.setFirstColumnSpanned(True)
        return item

    def add_tree_child(self, parent:QTreeWidgetItem, name:str, description:str):
        item = QTreeWidgetItem()
        item.setText(0, 'x2')
        item.setText(1, name)
        # item.setText(1, description)
        icon_provider = QFileIconProvider()
        file_icon = QIcon('guardian.png')
        item.setIcon(1, file_icon)
        parent.addChild(item)
        return item


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = Form()
    form.show()
exit(app.exec_())