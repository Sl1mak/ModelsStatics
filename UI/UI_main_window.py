from PyQt5.QtWidgets import (
    QWidget, QDesktopWidget, QPushButton, QMessageBox, QVBoxLayout, QFileDialog, QLabel, QHBoxLayout
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self.model_layout = QHBoxLayout()
        self.file_layout = QHBoxLayout()

        self.model_name = QLabel("Выберите модель", self)
        self.model_button = QPushButton("Выбрать...", self)
        self.file_name = QLabel("Выберите файл", self)
        self.file_button = QPushButton("Выбрать...", self)
        self.start_btn = QPushButton("Start", self)
        self.init_ui()

    def init_ui(self):
        self.resize(800, 600)
        self.center()

        self.model_button.clicked.connect(lambda: self.open_name_file_dialog(self.model_name))
        self.file_button.clicked.connect(lambda: self.open_name_file_dialog(self.file_name))
        self.start_btn.clicked.connect(self.start_process)
        self.setWindowTitle("ModelsStatics")

        self.model_layout.addWidget(self.model_button)
        self.model_layout.addWidget(self.model_name)
        self.file_layout.addWidget(self.file_button)
        self.file_layout.addWidget(self.file_name)
        self.main_layout.addLayout(self.model_layout)
        self.main_layout.addLayout(self.file_layout)
        self.main_layout.addWidget(self.start_btn)

        self.setLayout(self.main_layout)

    def open_name_file_dialog(self, target_label):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose file")

        if file_path:
            target_label.setText(file_path)

    def center(self):
        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_process(self):
        QMessageBox.information(self, "Info", "Start process")