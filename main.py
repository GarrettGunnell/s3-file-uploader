import sys
from PyQt5.QtWidgets import *

class FileUploader(QWidget):

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("File Uploader")

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("AAAAAAAAAA"))
        self.setLayout(layout)

app = QApplication([])
with open("stylesheet.qss", "r") as fh:
    app.setStyleSheet(fh.read())
fileUploader = FileUploader()
fileUploader.show()
sys.exit(app.exec_())