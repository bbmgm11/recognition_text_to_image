from PyQt5 import QtWidgets, QtGui, QtCore
import easyocr
import os
import cv2
import translators
from PIL import ImageGrab


class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Распознавание текста")
        self.resize(750, 700)

        self.setWindowFlag(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAcceptDrops(True)
        self.center()

        # основной фрейм на котором все кнопки, лайбл и фрейм 3
        self.frame_4 = QtWidgets.QFrame(self)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 728, 700))
        self.frame_4.setStyleSheet("QFrame{\n"
                                   "    color: white;\n"
                                   "    border-radius: 7px;\n"
                                   "    background-color: #032040;\n"
                                   "}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)

        # фрейм на котором кнопки закрыть и свернуть
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 728, 30))
        self.frame_3.setStyleSheet("QFrame{\n"
                                   "    border-bottom-left-radius: 0px;\n"
                                   "    border-bottom-right-radius: 0px;\n"
                                   "    background-color: #6495ed;\n"
                                   "}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)

        # кнопка закрытия
        self.pushButton_1 = QtWidgets.QPushButton("X", self.frame_3)
        self.pushButton_1.setGeometry(QtCore.QRect(687, 0, 41, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_1.setFont(font)
        self.pushButton_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_1.setStyleSheet("QPushButton{\n"
                                        "    color: white;\n"
                                        "    border: none;\n"
                                        "    border-top-right-radius: 7px;\n"
                                        "    background-color: #6495ed;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: #45494D;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed{\n"
                                        "    color: #EA2F4E;\n"
                                        "}")
        self.pushButton_1.clicked.connect(lambda: self.close())

        # кнопка сворачивания
        self.pushButton_2 = QtWidgets.QPushButton("_", self.frame_3)
        self.pushButton_2.setGeometry(QtCore.QRect(646, 0, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setStyleSheet("QPushButton{\n"
                                        "    color: white;\n"
                                        "    border: none;\n"
                                        "    background-color: #6495ed;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover{\n"
                                        "    background-color: #45494D;\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:pressed{\n"
                                        "    color: #EA2F4E;\n"
                                        "}")
        self.pushButton_2.setDefault(False)
        self.pushButton_2.clicked.connect(lambda: self.showMinimized())

        # лайбл
        self.image_label = QtWidgets.QLabel(self.frame_4)
        self.image_label.setGeometry(QtCore.QRect(0, 30, 729, 556))
        image = QtGui.QPixmap("icon/download.png")
        self.image_label.setPixmap(image)
        self.image_label.setScaledContents(True)
        self.image_label.setWordWrap(False)

        # кнопка выбрать изображение
        self.load_button = QtWidgets.QPushButton("Выбрать изображение", self.frame_4)
        self.load_button.setGeometry(QtCore.QRect(10, 610, 261, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.load_button.setFont(font)
        self.load_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load_button.setStyleSheet("QPushButton{\n"
                                       "    color: white;\n"
                                       "    border-radius: 7px;\n"
                                       "    background-color: #6495ed;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover{\n"
                                       "    background-color: #50566E;\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:pressed{\n"
                                       "    background-color: #434965;\n"
                                       "}")
        self.load_button.clicked.connect(self.image_loade)

        # кнопка распознавания
        self.decode_button = QtWidgets.QPushButton("Распознать", self.frame_4)
        self.decode_button.setGeometry(QtCore.QRect(10, 650, 261, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.decode_button.setFont(font)
        self.decode_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.decode_button.setStyleSheet("QPushButton{\n"
                                         "    color: white;\n"
                                         "    border-radius: 7px;\n"
                                         "    background-color: #6495ed;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "    background-color: #50566E;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed{\n"
                                         "    background-color: #434965;\n"
                                         "}")
        self.decode_button.clicked.connect(self.text_recognize)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.frame_4)

        # кнопка перевода
        self.decode_translate = QtWidgets.QPushButton("Перевести", self.frame_4)
        self.decode_translate.setGeometry(QtCore.QRect(450, 665, 271, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.decode_translate.setFont(font)
        self.decode_translate.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.decode_translate.setStyleSheet("QPushButton{\n"
                                            "    color: white;\n"
                                            "    border-radius: 7px;\n"
                                            "    background-color: #6495ed;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:hover{\n"
                                            "    background-color: #50566E;\n"
                                            "}\n"
                                            "\n"
                                            "QPushButton:pressed{\n"
                                            "    background-color: #434965;\n"
                                            "}")
        self.decode_translate.clicked.connect(self.translator)

        # лайот
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.frame_4)

        # кнопка ru и en и лейб выбора языка
        self.lang_sel = QtWidgets.QLabel("Язык текста:", self.frame_4)
        self.lang_sel.setGeometry(QtCore.QRect(450, 620, 271, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lang_sel.setFont(font)

        self.ru_button = QtWidgets.QRadioButton("Русский", self.frame_4)
        self.ru_button.setGeometry(QtCore.QRect(590, 640, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ru_button.setFont(font)
        self.ru_button.setStyleSheet("QRadioButton{\n"
                                     "    color: white;\n"
                                     "    border-radius: 7px;\n"
                                     "}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/Russia.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ru_button.setIcon(icon1)
        self.ru_button.setChecked(True)

        self.en_button = QtWidgets.QRadioButton("Английский", self.frame_4)
        self.en_button.setGeometry(QtCore.QRect(450, 640, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.en_button.setFont(font)
        self.en_button.setStyleSheet("QRadioButton{\n"
                                     "    color: white;\n"
                                     "    border-radius: 7px;\n"
                                     "}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/UnitedKingdom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.en_button.setIcon(icon)

        # контр в + контрл с
        self.shortcut_open = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+V"), self)
        self.shortcut_open.activated.connect(self.pasteImage)

        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.setPixmap(QtGui.QPixmap())

    # загрузка изображения через кнопку
    def image_loade(self):
        file_dealog = QtWidgets.QFileDialog()
        file_puth, _ = file_dealog.getOpenFileName(self, "Выберите изображение")

        if file_puth:
            pixmap = QtGui.QPixmap(file_puth)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)

    # распознавание
    def text_recognize(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            image = pixmap.toImage()
            image.save("temp.png")
            img = cv2.imread("temp.png")
            reader = easyocr.Reader(["ru", "en"])
            resault = reader.readtext(img, detail=0, paragraph=True)

            with open("result.txt", "w") as file:
                for line in resault:
                    file.write(f"{line}\n\n")
            os.startfile("result.txt")
            os.remove("temp.png")

    # перетаскивание безрамочного окна
    def center(self):
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

        except AttributeError:
            pass

    # дроп
    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.image_label.setPixmap(QtGui.QPixmap(file_path))
            event.accept()
        else:
            event.ignore()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    #  перевод
    def translator(self):
        pixmap = self.image_label.pixmap()
        if pixmap:
            image = pixmap.toImage()
            image.save("temp.png")
            img = cv2.imread("temp.png")
            reader = easyocr.Reader(["ru", "en"])
            resault = reader.readtext(img, detail=0, paragraph=True)

            with open("result.txt", "w") as file:
                for line in resault:
                    file.write(f"{line}\n\n")
            file_patch = os.path.join("result.txt")
            with open(file_patch, "r") as file:
                file_content = file.read()

            if self.ru_button.isChecked() == True:
                self.trans_resault = translators.translate_text(query_text=file_content, translator="google",
                                                                from_language="ru", to_language="en")

            elif self.en_button.isChecked() == True:
                self.trans_resault = translators.translate_text(query_text=file_content, translator="google",
                                                                from_language="en", to_language="ru")

            with open("translation.txt", "w") as file:
                for line in self.trans_resault:
                    file.write(f"{line}")

            os.remove("result.txt")
            os.startfile("translation.txt")
            os.remove("temp.png")

    def pasteImage(self):
        img = ImageGrab.grabclipboard()
        print(img)

    #   pixmap = QtGui.QPixmap(img)
    #   self.image_label.setPixmap(img)
    #   self.image_label.setScaledContents(True)

    def closeApp(self):
        app.quit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())
