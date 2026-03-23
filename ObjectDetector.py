import cv2 as cv
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class ObjectDetector:
    def __init__ (self, model_path, threshold = 0.5):
        self.model_path = model_path
        self.threshold = threshold

        base_options = python.BaseOptions(model_asset_path='models/efficientdet.tflite')
        options = vision.ObjectDetectorOptions(
            base_options=base_options,
            score_threshold=0.5,
        )
        self.detector = vision.ObjectDetector.create_from_options(options)

    def visualize(self, image, detections) -> np.ndarray:
        MARGIN = 10
        ROW_SIZE = 10
        FONT_SIZE = 3
        TEXT_COLOR = (0, 0, 0)

        for detection in detections.detections:
            category = detection.categories[0]
            category_name = category.category_name
            probality = round(category.score, 2)

            if probality < 0.6:
                TEXT_COLOR = (0, 0, 255)
            elif probality < 0.75:
                TEXT_COLOR = (0, 255, 255)
            else:
                TEXT_COLOR = (0, 255, 0)

            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            overlay = image.copy()
            cv.rectangle(overlay, start_point, end_point, TEXT_COLOR, -1)
            image = cv.addWeighted(image, 0.5, overlay, 0.5, 0)
            cv.rectangle(image, start_point, end_point, TEXT_COLOR, 2)

            result_text = category_name + ' (' + str(probality) + ')'
            text_location = (MARGIN + bbox.origin_x, MARGIN + ROW_SIZE + bbox.origin_y)
            cv.putText(image, result_text, text_location, cv.FONT_HERSHEY_COMPLEX, FONT_SIZE, TEXT_COLOR, 2)

        return image
    
    def process(self, image):
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)

        detection_result = self.detector.detect(image)

        image_copy = np.copy(image.numpy_view())
        return self.visualize(image_copy, detection_result)