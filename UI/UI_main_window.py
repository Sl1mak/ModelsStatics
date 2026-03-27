from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QPushButton, QMessageBox


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.start_btn = QPushButton("Start", self)
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.center()

        self.start_btn.clicked.connect(self.start_process)
        self.setWindowTitle("ModelsStatics")

    def center(self):
        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_process(self):
        QMessageBox.information(self, "Info", "Start process")