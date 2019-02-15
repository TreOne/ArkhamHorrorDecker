from PyQt5 import QtCore, QtGui, QtWidgets
from Utility.AHDObserver import AHDObserver
from Utility.AHDMeta import AHDMeta
from View.MainWindow import Ui_MainWindow


class AHDView(Ui_MainWindow, AHDObserver, metaclass=AHDMeta):
    """
    Класс отвечающий за визуальное представление AHDModel.
    """

    def __init__(self, in_controller, in_model, parent=None):
        """
        Конструктор принимает ссылки на модель и контроллер.
        """
        super(Ui_MainWindow, self).__init__(parent)
        self.mController = in_controller
        self.mModel = in_model

        # подключаем визуальное представление
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # регистрируем представление в качестве наблюдателя
        self.mModel.addObserver(self)

        # связываем событие завершения редактирования с методом контроллера
        self.connect(self.ui.le_c, SIGNAL("editingFinished()"),
                     self.mController.setC)
        self.connect(self.ui.le_d, SIGNAL("editingFinished()"),
                     self.mController.setD)

    def model_is_changed(self):
        """
        Метод вызывается при изменении модели.
        Запрашивает и отображает значение суммы.
        """
        sum = str(self.mModel.sum)
        self.ui.le_result.setText(sum)
