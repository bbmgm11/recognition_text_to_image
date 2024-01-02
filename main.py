from PyQt5 import QtWidgets, QtGui
import easyocr
import os
import cv2

class Interface(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Распознавание текста")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.image_label = QtWidgets.QLabel(self)
        self.load_button = QtWidgets.QPushButton("Выбрать изображение", self)
        self.load_button.clicked.connect(self.image_loade)
        self.decode_button = QtWidgets.QPushButton("Распознать", self)
        self.decode_button.clicked.connect(self.text_recognize)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_button)
        layout.addWidget(self.decode_button)

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
            reader = easyocr.Reader(["ru"])
            resault = reader.readtext(img, detail=0, paragraph=True)

            with open("result.txt", "w") as file:
                for line in resault:
                    file.write(f"{line}\n\n")
            os.startfile("result.txt")
            os.remove("temp.png")




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = Interface()
    window.show()
    sys.exit(app.exec_())