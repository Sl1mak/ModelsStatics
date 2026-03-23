import cv2 as cv
import numpy as np
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

def visualize(image, detections) -> np.ndarray:
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

start = time.time()

base_options = python.BaseOptions(model_asset_path='models/efficientdet.tflite')
options = vision.ObjectDetectorOptions(
    base_options=base_options,
    score_threshold=0.5,
)
detector = vision.ObjectDetector.create_from_options(options)

cap = cv.VideoCapture('assets/1.mp4')

fourcc = cv.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv.CAP_PROP_FPS)
out = cv.VideoWriter('result.mp4', fourcc, fps, (width, height))

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # frame_count += 1
    # if frame_count % 3 != 0:
    #     continue

    image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

    detection_result = detector.detect(image)

    image_copy = np.copy(image.numpy_view())
    annotated_image = visualize(image_copy, detection_result)

    cv.imshow('frame', annotated_image)
    out.write(annotated_image)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

end = time.time()
fps = 1 / (end - start)
print("Code complete in ", end - start, "s")
print("FPS: ", fps)