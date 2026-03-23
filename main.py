import time
from ObjectDetector import ObjectDetector

start = time.time()

detector = ObjectDetector('models/efficientdet.tflite')

cap = cv.VideoCapture('assets/test.mp4')

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

    frame_count += 1
    if frame_count % 3 != 0:
        continue

    processed = detector.process(frame)

    cv.imshow('frame', processed)
    out.write(processed)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

end = time.time()
fps = 1 / (end - start)
print("Code complete in ", end - start, "s")
print("FPS: ", fps)