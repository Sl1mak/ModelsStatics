class BaseDetector:
    def __init__(self, model_path=None, threshold = 0.5):
        self.model_path = model_path
        self.threshold = threshold

    def detect(self, image):
        raise NotImplementedError("detect() must be implemented")