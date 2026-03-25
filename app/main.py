from core.detectors.mediapipe_detector import MediapipeDetector
from core.pipelines.Video_pipeline import VideoPipeline
from core.visualize.drawer import Drawer

detector = MediapipeDetector("../models/efficientdet.tflite")
drawer = Drawer()
print(detector)
print(drawer)

pipeline = VideoPipeline("../assets/test_tg.mp4", detector, drawer, output_path="result.mp4")
pipeline.process()
print(pipeline)
