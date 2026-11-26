from PySide6.QtWidgets import QApplication, QWidget, QLabel
from PySide6.QtGui import QPixmap


class AboutWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('About Me')
        self.setGeometry(200, 200, 360, 440)

        self.my_name = QLabel('Yuval Barkai', self)
        self.my_name.setGeometry(20, 20, 300, 25)

        self.my_email = QLabel('yuval.barkai@s.afeka.ac.il', self)
        self.my_email.setGeometry(20, 50, 300, 25)

        self.linkedin_label = QLabel('<a href="https://www.linkedin.com/in/yuval-barkai1/">LinkedIn Profile</a>', self)
        self.linkedin_label.setOpenExternalLinks(True)
        self.linkedin_label.setGeometry(20, 80, 300, 25)

        self.my_picture = QLabel(self)
        self.my_picture.setGeometry(20, 115, 300, 300)

        image = QPixmap('albert-einstein-sticking-out-tongue_c.JPG').scaled(300, 300)
        self.my_picture.setPixmap(image)


if __name__ == '__main__':
    app = QApplication()
    window = AboutWindow()
    window.show()
    app.exec()