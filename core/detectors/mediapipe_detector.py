import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from core.detectors.base_detector import BaseDetector

class MediapipeDetector(BaseDetector):
    def __init__(self, model_path, threshold = 0.5):
        super().__init__(model_path, threshold)

        base_options = python.BaseOptions(model_asset_path = model_path)
        options = vision.ObjectDetectorOptions(
            base_options = base_options,
            score_threshold = threshold,
        )

        self.detector = vision.ObjectDetector.create_from_options(options)

    def detect(self, image):
        mp_image = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = image,
        )

        detection_result = self.detector.detect(mp_image)

        results = []

        for detection in detection_result.detections:
            category = detection.categories[0]
            bbox = detection.bounding_box

            results.append({
                "label": category.category_name,
                "score": float(category.score),
                "bbox": [
                    bbox.origin_x,
                    bbox.origin_y,
                    bbox.width,
                    bbox.height
                ]
            })

        return results