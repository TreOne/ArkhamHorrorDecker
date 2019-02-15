"""
Модуль реализации метакласса, необходимого для работы представления.

pyqtWrapperType - метакласс общий для оконных компонентов Qt.
ABCMeta - метакласс для реализации абстрактных суперклассов.

AHDMeta - метакласс для представления.
"""

from PyQt5.QtCore import pyqtWrapperType
from abc import ABCMeta


class AHDMeta(pyqtWrapperType, ABCMeta):
    pass
