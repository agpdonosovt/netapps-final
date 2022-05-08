# Souvenir Client v0.1
# Écrit par Alejandro Garcia
#
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from requests.auth import HTTPBasicAuth
from io import BytesIO
import sys
import pyaudio
import wave
import requests
import os

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
IP = '0.0.0.0'
PORT = '19720'
souvenir_user = ''
souvenir_passwd = ''


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Souvenir')
        self.setMinimumSize(600, 600)
        self.setMaximumSize(600, 600)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(65, 179, 211))
        palette.setColor(QPalette.WindowText, QColor(228, 288, 288))
        palette.setColor(QPalette.Base, QColor(228, 228, 228))
        palette.setColor(QPalette.PlaceholderText, QColor(132, 199, 220))
        palette.setColor(QPalette.Text, QColor(65, 179, 211))
        palette.setColor(QPalette.ButtonText, QColor(65, 179, 211))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        font = QFont("Helvetica", 15)

        self.setStyleSheet("QLineEdit {"
                           "border : 5px;"
                           "border-radius : 10;"
                           "color: rgb(65, 179, 211);"
                           "}"
                           "QPushButton {"
                           "color: rgb(65, 179, 211);"
                           "}"
                           )

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
        submit_btn.setFocusPolicy(Qt.NoFocus)

    def check_pass(self):

        url = 'http://' + IP + ':' + PORT + '/login'  # change ip to raspberrypi

        try:
            login_request = requests.get(url, auth=HTTPBasicAuth(self.user_label.text(),
                                                                 self.pass_label.text()))

            global souvenir_user
            global souvenir_passwd
            souvenir_user = self.user_label.text()
            souvenir_passwd = self.pass_label.text()

            if login_request.status_code != 200:
                button = QMessageBox.warning(self, 'Invalid Login', 'Invalid login. '
                                                                    'Try again with different credentials')
                self.user_label.clear()
                self.pass_label.clear()
            else:
                self.switch_window()

        except requests.exceptions.ConnectionError:
            button = QMessageBox.warning(self, 'Connection Failed', 'Could not find local Souvenir server.')
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

        self.setStyleSheet("QLineEdit {"
                           "border : 5px;"
                           "border-radius : 10;"
                           "color: rgb(65, 179, 211);"
                           "}"
                           "QPushButton {"
                           "color: rgb(65, 179, 211);"
                           "}"
                           )

        font = QFont("Helvetica", 15)

        self.pixmap = QPixmap('logo.png')
        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.setGeometry(50, 80, 500, 300)

        rec_btn = QPushButton(self)
        rec_btn.setText('Record Audio')
        rec_btn.setFont(font)
        rec_btn.setGeometry(150, 400, 120, 30)
        rec_btn.setFocusPolicy(Qt.NoFocus)
        rec_btn.clicked.connect(self.rec_click)

        play_btn = QPushButton(self)
        play_btn.setText('Play Audio')
        play_btn.setFont(font)
        play_btn.setGeometry(330, 400, 120, 30)
        play_btn.setFocusPolicy(Qt.NoFocus)
        play_btn.clicked.connect(self.get_click)

    def rec_click(self):
        souvenir.setCurrentWidget(record)

    def get_click(self):
        souvenir.setCurrentWidget(play)


class RecordWindow(QMainWindow):
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

        self.setStyleSheet("QLineEdit {"
                           "border : 5px;"
                           "border-radius : 10;"
                           "color: rgb(65, 179, 211);"
                           "}"
                           "QPushButton {"
                           "color: rgb(65, 179, 211);"
                           "}"
                           )

        font = QFont("Helvetica", 15)

        self.audio_title = QLineEdit(self)
        self.audio_title.setPlaceholderText('Audio Title')
        self.audio_title.setFont(font)
        self.audio_title.setGeometry(150, 400, 300, 25)

        self.collection = QLineEdit(self)
        self.collection.setPlaceholderText('Collection')
        self.collection.setFont(font)
        self.collection.setGeometry(150, 440, 300, 25)

        self.duration = QLineEdit(self)
        self.duration.setPlaceholderText('Time - Maximum of 60 seconds')
        self.duration.setFont(font)
        self.duration.setGeometry(150, 480, 300, 25)

        self.pixmap = QPixmap('logo.png')
        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.setGeometry(50, 80, 500, 300)

        self.submit_btn = QPushButton(self)
        self.submit_btn.setText('Record')
        self.submit_btn.setFont(font)
        self.submit_btn.setGeometry(225, 515, 150, 30)
        self.submit_btn.clicked.connect(self.rec_click)
        self.submit_btn.setFocusPolicy(Qt.NoFocus)

        self.help_btn = QPushButton(self)
        self.help_btn.setText('Help')
        self.help_btn.setFont(font)
        self.help_btn.setGeometry(15, 560, 80, 30)
        self.help_btn.clicked.connect(self.help)
        self.help_btn.setFocusPolicy(Qt.NoFocus)

        self.back_btn = QPushButton(self)
        self.back_btn.setText('Back')
        self.back_btn.setFont(font)
        self.back_btn.setGeometry(15, 520, 80, 30)
        self.back_btn.clicked.connect(self.back)
        self.back_btn.setFocusPolicy(Qt.NoFocus)

    def rec_click(self):

        title = self.audio_title.text()
        collection = self.collection.text()
        secs = self.duration.text()

        if secs.isnumeric() and title and collection and 0 < int(secs) <= 60:
            self.record_audio()
        else:
            button = QMessageBox.information(self, 'Audio Info', 'Enter a title and a collection to save audio.\n'
                                                                 'Make sure to enter an integer duration for seconds.')

    def record_audio(self):

        self.p = pyaudio.PyAudio()

        title = self.audio_title.text() + '.wav'
        collection = self.collection.text()
        secs = int(self.duration.text())

        self.record(title, secs)

        self.submit_btn.setText('Stopped')

        try:
            files = {'file': open(os.getcwd() + '/temp/' + title, 'rb')}
            url = 'http://' + IP + ':' + PORT + '/upload?title=' + title + '&collection=' + collection
            post = requests.post(url, auth=HTTPBasicAuth(souvenir_user, souvenir_passwd),
                                 files=files)

            if post.status_code == 201:
                button = QMessageBox.information(self, 'Success', 'Uploaded audio to server!')
            else:
                button = QMessageBox.warning(self, 'Failure', 'Could not upload file to server.')

            os.remove(os.getcwd() + '/temp/' + title)

        except requests.exceptions.ConnectionError:
            button = QMessageBox.warning(self, 'Connection Failed', 'Could not find local Souvenir server.')

        self.audio_title.clear()
        self.collection.clear()
        self.duration.clear()
        self.submit_btn.setText('Record')
        self.return_to_self()

    def record(self, file, secs):

        dur = secs

        self.stream = self.p.open(format=FORMAT, channels=CHANNELS,
                                  rate=RATE, input=True, frames_per_buffer=CHUNK)
        self.frames = []

        for i in range(0, int(RATE / CHUNK * secs)):
            data = self.stream.read(CHUNK)
            self.frames.append(data)

        sample_width = self.p.get_sample_size(FORMAT)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

        path = os.getcwd() + '/temp/' + file
        wf = wave.open(path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(sample_width)
        wf.setframerate(RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def help(self):
        button = QMessageBox.information(self, 'Audio Info',
                                         'Enter an audio title, collection, and duration.' +
                                         'Then, press record, and begin speaking. The wheel will spin ' +
                                         'for the duration of the recording, and when it stops spinning, ' +
                                         'the recording is done.')

    def check_button(self, audio, audio_proc):
        while not self.submit_btn.isChecked() or not audio_proc.is_alive():
            audio.stop(self.audio_title.text())

    def return_to_self(self):
        souvenir.setCurrentWidget(self)

    def back(self):
        souvenir.setCurrentWidget(choice)


class PlayWindow(QMainWindow):
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

        self.setStyleSheet("QLineEdit {"
                           "border : 5px;"
                           "border-radius : 10;"
                           "color: rgb(65, 179, 211);"
                           "}"
                           "QPushButton {"
                           "color: rgb(65, 179, 211);"
                           "}"
                           )

        font = QFont("Helvetica", 15)

        self.audio_title = QLineEdit(self)
        self.audio_title.setPlaceholderText('Audio Title')
        self.audio_title.setFont(font)
        self.audio_title.setGeometry(150, 400, 300, 25)

        self.collection = QLineEdit(self)
        self.collection.setPlaceholderText('Collection')
        self.collection.setFont(font)
        self.collection.setGeometry(150, 440, 300, 25)

        self.pixmap = QPixmap('logo.png')
        self.img_label = QLabel(self)
        self.img_label.setPixmap(self.pixmap)
        self.img_label.setGeometry(50, 80, 500, 300)

        self.submit_btn = QPushButton(self)
        self.submit_btn.setText('Play')
        self.submit_btn.setFont(font)
        self.submit_btn.setGeometry(225, 475, 150, 30)
        self.submit_btn.clicked.connect(self.find_audio)  #
        self.submit_btn.setFocusPolicy(Qt.NoFocus)

        self.help_btn = QPushButton(self)
        self.help_btn.setText('Help')
        self.help_btn.setFont(font)
        self.help_btn.setGeometry(15, 560, 80, 30)
        self.help_btn.clicked.connect(self.help)
        self.help_btn.setFocusPolicy(Qt.NoFocus)

        self.back_btn = QPushButton(self)
        self.back_btn.setText('Back')
        self.back_btn.setFont(font)
        self.back_btn.setGeometry(15, 520, 80, 30)
        self.back_btn.clicked.connect(self.back)
        self.back_btn.setFocusPolicy(Qt.NoFocus)

    def find_audio(self):
        title = self.audio_title.text()
        collection = self.collection.text()

        try:
            url = 'http://' + IP + ':' + PORT + '/download?title=' + title + '&collection=' + collection
            result = requests.get(url, auth=HTTPBasicAuth(souvenir_user, souvenir_passwd))

            if result.status_code != 404:

                audio_file = BytesIO(result.content)

                with open(title, "wb") as f:
                    f.write(audio_file.getbuffer())

                os.rename(title, os.getcwd() + '/temp/' + title + '.wav')

                self.play_audio(os.getcwd() + '/temp/' + title + '.wav')

                os.remove(os.getcwd() + '/temp/' + title + '.wav')

                self.audio_title.clear()
                self.collection.clear()
                self.return_to_self()

            else:
                button = QMessageBox.warning(self, 'File not Found', 'The requested file was not found on the server.')

        except requests.exceptions.ConnectionError:
            button = QMessageBox.warning(self, 'Connection Failed', 'Could not find local Souvenir server.')
            self.audio_title.clear()
            self.collection.clear()

    def play_audio(self, title):

        self.p = pyaudio.PyAudio()

        self.wf = wave.open(title, 'rb')

        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(), rate=self.wf.getframerate(),
                                  output=True)

        data = self.wf.readframes(CHUNK)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(CHUNK)
            if data == b'':
                break

        self.stream.close()
        self.p.terminate()

        button = QMessageBox.warning(self, 'Audio', 'Finished Playing Audio')

    def help(self):
        button = QMessageBox.information(self, 'Audio Info',
                                         'Enter an audio title and collection to search.' +
                                         'Then, press play, and if the audio is found, the audio ' +
                                         'will begin playing.')

    def back(self):
        souvenir.setCurrentWidget(choice)

    def return_to_self(self):
        souvenir.setCurrentWidget(self)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    if not os.path.exists(os.getcwd() + '/temp'):
        os.mkdir(os.getcwd() + '/temp')

    app = QApplication(sys.argv)
    souvenir = QStackedWidget()
    souvenir.setFocusPolicy(Qt.NoFocus)

    login = LoginWindow()
    souvenir.addWidget(login)

    choice = ChoiceWindow()
    souvenir.addWidget(choice)

    record = RecordWindow()
    souvenir.addWidget(record)

    play = PlayWindow()
    souvenir.addWidget(play)

    souvenir.setCurrentWidget(login)
    souvenir.show()

    sys.exit(app.exec_())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
