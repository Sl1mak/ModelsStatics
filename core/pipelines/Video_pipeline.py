import cv2 as cv

class VideoPipeline:
    def __init__(self, video_path, detector, drawer, output_path = "../result.mp4", skip_frames = 1):
        self.cap = cv.VideoCapture(video_path)
        self.detector = detector
        self.drawer = drawer
        self.skip_frames = skip_frames

        fourcc = cv.VideoWriter.fourcc(*'mp4v')
        width = int(self.cap.get(cv.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = self.cap.get(cv.CAP_PROP_FPS)
        self.out = cv.VideoWriter(output_path, fourcc, fps, (width, height))

        self.frame_count = 0

    def process(self):
        frames = []
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.frame_count += 1
            if self.frame_count % self.skip_frames != 0:
                continue

            detections = self.detector.detect(frame)
            frame = self.drawer.draw(frame, detections)
            self.out.write(frame)

            frames.append(frame)

        self.cap.release()
        self.out.release()
        return frames