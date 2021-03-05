import sys
import os
import boto3
import json
from PyQt5.QtWidgets import *

class FileUploader(QWidget):

    def __init__(self, s3, table):
        super().__init__()
        self.s3 = s3
        self.table = table
        self.setGeometry(200, 200, 300, 200)
        self.setWindowTitle("File Uploader")
        self.center()

        self.initUI()

    def initUI(self):
        overallLayout = QVBoxLayout()
        uploadLayout = QHBoxLayout()
        uploadLayout.addSpacing(10)
        
        self.uploadMp3Button = QPushButton("Upload .mp3")
        self.uploadMp3Button.clicked.connect(self.uploadMp3)
        uploadLayout.addWidget(self.uploadMp3Button, 1)
        uploadLayout.addSpacing(10)

        self.uploadAlbumButton = QPushButton("Upload Album")
        self.uploadAlbumButton.clicked.connect(self.uploadAlbum)
        uploadLayout.addWidget(self.uploadAlbumButton, 1)
        uploadLayout.addSpacing(10)
        
        self.uploadArtistButton = QPushButton("Upload Artist")
        self.uploadArtistButton.clicked.connect(self.uploadArtist)
        uploadLayout.addWidget(self.uploadArtistButton, 1)
        uploadLayout.addSpacing(10)
        overallLayout.addLayout(uploadLayout)
        genreLayout = QHBoxLayout()
        genreLayout.addStretch(1)
        self.genreBox = QLineEdit()
        genreLayout.addWidget(QLabel("Genre:"))
        genreLayout.addWidget(self.genreBox)
        genreLayout.addStretch(1)
        overallLayout.addLayout(genreLayout)
        
        self.setLayout(overallLayout)

    def center(self):
        qr = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(centerPoint)
        self.move(qr.topLeft())

    def uploadMp3(self):
        fp = QFileDialog.getOpenFileName(self, 'Open file', 'C:\\', "mp3 files (*.mp3)")[0]
        if fp == '' or fp.split('.')[-1] != 'mp3': return
        song = fp.split('/')[-1]
        data = open(fp, 'rb')
        s3.Bucket('cs493-gunnellg-bucket').put_object(Key=song, Body=data)
        data.close()

    def uploadAlbum(self):
        dp = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dp == '': return
        album = dp.split('/')[-1]
        for song in os.listdir(dp):
            if song.split('.')[-1] != 'mp3': continue
            fp = dp + '/' + song
            data = open(fp, 'rb')
            key = album + '/' + song
            s3.Bucket('cs493-gunnellg-bucket').put_object(Key=key, Body=data)
            data.close()
    
    def uploadArtist(self):
        dp = QFileDialog.getExistingDirectory(self, "Select Directory")
        if dp == '': return
        artist = dp.split('/')[-1]
        for album in os.listdir(dp):
            path = dp + '/' + album
            if os.path.isfile(path): continue
            for song in os.listdir(path):
                fp = path + '/' + song
                if song.split('.')[-1] != 'mp3': continue
                data = open(fp, 'rb')
                key = artist + '/' + album + '/' + song
                table_item = {
                    'genre': self.genreBox.text(),
                    'artist_album_song': artist + '_' + album + '_' + song.split('.mp3')[0],
                    'artist': artist,
                    'album': album,
                    'song': song.split('.mp3')[0],
                    'info': {
                        's3_key': key
                    }
                }
                table.put_item(Item=table_item)
                s3.Bucket('cs493-gunnellg-bucket').put_object(Key=key, Body=data)
                data.close()


app = QApplication([])
session = boto3.session.Session()
s3 = session.resource('s3')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('music')
with open("stylesheet.qss", "r") as fh:
    app.setStyleSheet(fh.read())
fileUploader = FileUploader(s3, table)
fileUploader.show()

sys.exit(app.exec_())