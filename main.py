import sys
import os
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
        self.uploadMp3Button.clicked.connect(self.uploadMp3)
        layout.addWidget(self.uploadMp3Button, 1)
        layout.addSpacing(10)

        self.uploadAlbumButton = QPushButton("Upload Album")
        self.uploadAlbumButton.clicked.connect(self.uploadAlbum)
        layout.addWidget(self.uploadAlbumButton, 1)
        layout.addSpacing(10)
        
        self.uploadArtistButton = QPushButton("Upload Artist")
        self.uploadArtistButton.clicked.connect(self.uploadArtist)
        layout.addWidget(self.uploadArtistButton, 1)
        layout.addSpacing(10)
        
        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerPoint)
        self.move(qr.topLeft())

    def uploadMp3(self):
        fp = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', "mp3 files (*.mp3)")[0]
        if fp == '': return
        songName = fp.split('/')[-1]
        data = open(fp, 'rb')
        s3.Bucket('cs493-gunnellg-bucket').put_object(Key=songName, Body=data)
        data.close()

    def uploadAlbum(self):
        dp = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dp == '': return
        dname = dp.split('/')[-1]
        for filename in os.listdir(dp):
            if filename.split('.')[-1] != 'mp3': continue
            fp = dp + '/' + filename
            data = open(fp, 'rb')
            key = dname + '/' + filename
            s3.Bucket('cs493-gunnellg-bucket').put_object(Key=key, Body=data)
            data.close()
    
    def uploadArtist(self):
        dp = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dp == '': return
        dname = dp.split('/')[-1]
        for album in os.listdir(dp):
            path = dp + '/' + album
            if os.path.isfile(path): continue
            for song in os.listdir(path):
                fp = path + '/' + song
                if song.split('.')[-1] != 'mp3': continue
                data = open(fp, 'rb')
                key = dname + '/' + album + '/' + song
                s3.Bucket('cs493-gunnellg-bucket').put_object(Key=key, Body=data)
                data.close()


app = QApplication([])
session = boto3.session.Session(profile_name='s3admin')
s3 = session.resource('s3')

with open("stylesheet.qss", "r") as fh:
    app.setStyleSheet(fh.read())

fileUploader = FileUploader(s3)
fileUploader.show()

sys.exit(app.exec_())