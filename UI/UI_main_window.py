from core.detectors.mediapipe_detector import MediapipeDetector
from core.pipelines.Video_pipeline import VideoPipeline
from core.visualize.drawer import Drawer

from PyQt5.QtWidgets import (
    QWidget, QDesktopWidget, QPushButton, QMessageBox, QFileDialog, QLabel, QHBoxLayout, QVBoxLayout, QGroupBox,
    QLineEdit, QSizePolicy
)
from PyQt5.QtCore import QThread, pyqtSignal

class VideoProcessingThread(QThread):
    finished = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, model_path, file_path):
        super().__init__()
        self.model_path = model_path
        self.file_path = file_path

    def run(self):
        try:
            detector = MediapipeDetector(self.model_path)
            drawer = Drawer()
            pipeline = VideoPipeline(self.file_path, detector, drawer, output_path="result.mp4")
            pipeline.process()

            self.finished.emit()

        except Exception as e:
            self.error_signal.emit(str(e))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 300)
        self.center()
        self.setWindowTitle("MS")

        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        self.files_group = QGroupBox("Input files")
        self.files_layout = QVBoxLayout()
        self.files_layout.setSpacing(15)

        self.model_row = QHBoxLayout()
        self.model_name = QLabel("Model:")
        self.model_name.setFixedWidth(60)
        self.model_path = QLineEdit()
        self.model_path.setPlaceholderText("Choose model file...")
        self.model_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.model_btn = QPushButton("...")
        self.model_btn.setFixedWidth(40)
        self.model_row.addWidget(self.model_name)
        self.model_row.addWidget(self.model_path)
        self.model_row.addWidget(self.model_btn)

        self.file_row = QHBoxLayout()
        self.file_name = QLabel("File:")
        self.file_name.setFixedWidth(60)
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Choose file...")
        self.file_path.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.file_btn = QPushButton("...")
        self.file_btn.setFixedWidth(40)
        self.file_row.addWidget(self.file_name)
        self.file_row.addWidget(self.file_path)
        self.file_row.addWidget(self.file_btn)

        self.files_layout.addLayout(self.model_row)
        self.files_layout.addLayout(self.file_row)
        self.files_group.setLayout(self.files_layout)

        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.addStretch()

        self.start_btn = QPushButton("Start")
        self.start_btn.setFixedSize(100, 30)

        self.bottom_layout.addWidget(self.start_btn)

        self.main_layout.addWidget(self.files_group)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.bottom_layout)

        self.setLayout(self.main_layout)

        self.start_btn.clicked.connect(self.start_process)

        self.model_btn.clicked.connect(
            lambda: self.open_name_file_dialog(
                self.model_path,
                title="Choose model file",
                filter="Model files (*.tflite *.oonx *.pt);; All files (*)"
            )
        )

        self.file_btn.clicked.connect(
            lambda: self.open_name_file_dialog(
                self.file_path,
                title="Choose file",
                filter="Media files (*.mp4 *.png *.jpg);; All files (*)"
            )
        )

    def open_name_file_dialog(self, target_widget, title="Choose file", filter="All files (*)"):
        file_path, _ = QFileDialog.getOpenFileName(self, title, "", filter)

        if file_path:
            target_widget.setText(file_path)

    def center(self):
        qr = self.geometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def start_process(self):
        model = self.model_path.text()
        file = self.file_path.text()

        if not model or not file:
            QMessageBox.critical(self, "Error", "Please choose model and file")
            return

        self.start_btn.setEnabled(False)
        self.start_btn.setText("Processing...")

        self.thread = VideoProcessingThread(model, file)
        self.thread.finished.connect(self.process_finished)
        self.thread.error_signal.connect(self.process_error)
        self.thread.start()

    def process_finished(self):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start")
        QMessageBox.information(self, "Success", "Processing finished")

    def process_error(self, error_message):
        self.start_btn.setEnabled(True)
        self.start_btn.setText("Start")
        QMessageBox.critical(self, "Error", error_message)