import sys

# from core.detectors.mediapipe_detector import MediapipeDetector
# from core.pipelines.Video_pipeline import VideoPipeline
# from core.visualize.drawer import Drawer
from UI.UI_main_window import MainWindow
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

# detector = MediapipeDetector("../models/efficientdet.tflite")
# drawer = Drawer()
# print(detector)
# print(drawer)
#
# pipeline = VideoPipeline("../assets/test_tg.mp4", detector, drawer, output_path="result.mp4")
# pipeline.process()
# print(pipeline)
