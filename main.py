from PyQt5 import QtWidgets, QtGui, QtCore
import easyocr
import os
import cv2

class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Распознавание текста")
        self.resize(750,700)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.center()

        #основной фрейм на котором все кнопки, лайбл и фрейм 3
        self.frame_4 = QtWidgets.QFrame(self)
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 750, 700))
        self.frame_4.setStyleSheet("QFrame{\n"
                                   "    color: white;\n"
                                   "    border-radius: 7px;\n"
                                   "    background-color: #032040;\n"
                                   "}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)


        #фрейм на котором кнопки закрыть и свернуть
        self.frame_3 = QtWidgets.QFrame(self.frame_4)
        self.frame_3.setGeometry(QtCore.QRect(0, 0, 728, 30))
        self.frame_3.setStyleSheet("QFrame{\n"
                                   "    border-bottom-left-radius: 0px;\n"
                                   "    border-bottom-right-radius: 0px;\n"
                                   "    background-color: #6495ed;\n"
                                   "}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)


        #кнопка закрытия
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

        #кнопка сворачиванья
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

        #лайбл
        self.image_label = QtWidgets.QLabel(self.frame_4)
        self.image_label.resize(751, 581)
        self.image_label.setGeometry(QtCore.QRect(0, 30, 741, 556))
        self.image_label.setTextFormat(QtCore.Qt.AutoText)
        self.image_label.setScaledContents(True)
        self.image_label.setWordWrap(False)

        #кнопка выбрать изображение
        self.load_button = QtWidgets.QPushButton("Выбрать изображение", self.frame_4)
        self.load_button.setGeometry(QtCore.QRect(250, 588, 261, 30))
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


        # кнопка распознования
        self.decode_button = QtWidgets.QPushButton("Распознать", self.frame_4)
        self.decode_button.setGeometry(QtCore.QRect(250, 623, 261, 30))
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



    def image_loade(self):
        file_dealog = QtWidgets.QFileDialog()
        file_puth, _ = file_dealog.getOpenFileName(self, "Выбирите изображение")

        if file_puth:
            pixmap = QtGui.QPixmap(file_puth)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)


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

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())