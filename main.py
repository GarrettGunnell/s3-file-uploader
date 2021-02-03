import sys
import boto3
from PyQt5.QtWidgets import *

class FileUploader(QWidget):

    def __init__(self, s3):
        super().__init__()
        self.s3 = s3
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("File Uploader")
        self.center()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.addSpacing(10)
        
        self.uploadMp3Button = QPushButton("Upload .mp3")
        layout.addWidget(self.uploadMp3Button, 1)
        layout.addSpacing(10)

        self.uploadAlbumButton = QPushButton("Upload Album")
        layout.addWidget(self.uploadAlbumButton, 1)
        layout.addSpacing(10)
        
        self.uploadArtistButton = QPushButton("Upload Artist")
        layout.addWidget(self.uploadArtistButton, 1)
        layout.addSpacing(10)
        
        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerPoint)
        self.move(qr.topLeft())

app = QApplication([])
session = boto3.session.Session(profile_name='s3admin')
s3 = session.resource('s3')

with open("stylesheet.qss", "r") as fh:
    app.setStyleSheet(fh.read())

fileUploader = FileUploader(s3)
fileUploader.show()

sys.exit(app.exec_())