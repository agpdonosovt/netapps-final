# Souvenir Client v0.1
# Écrit par Alejandro Garcia
#
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from requests.auth import HTTPBasicAuth
import sys
import pyaudio
import requests


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Souvenir')
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(65, 179, 211))
        palette.setColor(QPalette.WindowText, QColor(228, 288, 288))
        palette.setColor(QPalette.Base, QColor(65, 179, 211))
        palette.setColor(QPalette.PlaceholderText, QColor(228, 228, 228))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        font = QFont("Helvetica", 15)

        self.user_label = QLineEdit(self)
        self.user_label.setPlaceholderText('Username')
        self.user_label.setFont(font)
        self.user_label.setGeometry(150, 400, 300, 25)

        self.pass_label = QLineEdit(self)
        self.pass_label.setPlaceholderText('Password')
        self.pass_label.setFont(font)
        self.pass_label.setGeometry(150, 440, 300, 25)

        self.pixmap = QPixmap('logo.png')
        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.setGeometry(50, 80, 500, 300)

        submit_btn = QPushButton(self)
        submit_btn.setText('Login')
        submit_btn.setFont(font)
        submit_btn.setGeometry(225, 475, 150, 30)
        submit_btn.clicked.connect(self.check_pass)

    def check_pass(self):

        url = 'http://0.0.0.0:19720/login'  # change ip to raspberrypi

        try:
            login_request = requests.get(url, auth=HTTPBasicAuth(self.user_label.text(),
                                                                 self.pass_label.text()))

            if login_request.status_code != 200:
                button = QMessageBox.warning(self, 'Invalid Login', 'Try again with different credentials')
                self.user_label.clear()
                self.pass_label.clear()
            else:
                self.switch_window()

        except requests.exceptions.ConnectionError:
            button = QMessageBox.warning(self, 'Connection Failed', 'Could not find local souvenir server.')
            self.user_label.clear()
            self.pass_label.clear()

    def switch_window(self):
        souvenir.setCurrentWidget(choice)


class ChoiceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Souvenir')
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(65, 179, 211))
        palette.setColor(QPalette.WindowText, QColor(228, 288, 288))
        palette.setColor(QPalette.Base, QColor(65, 179, 211))
        palette.setColor(QPalette.PlaceholderText, QColor(228, 228, 228))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        font = QFont("Helvetica", 15)

        self.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    souvenir = QStackedWidget()

    login = LoginWindow()
    souvenir.addWidget(login)

    choice = ChoiceWindow()
    souvenir.addWidget(choice)

    souvenir.setCurrentWidget(login)
    souvenir.show()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
