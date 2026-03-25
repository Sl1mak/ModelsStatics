import cv2 as cv

class Drawer:
    def __init__(self, config=None):
        self.config = config or {
            "font_scale": 1,
            "thickness": 2,
            "margin": 5
        }

    def get_color(self, score):
        if score < 0.6:
            return (0, 0, 255)
        elif score < 0.75:
            return (0, 255, 255)
        else:
            return (0, 255, 255)

    def draw(self, image, detections):
        for det in detections:
            x, y, w, h = det["bbox"]
            label = det["label"]
            score = round(det["score"], 2)

            color = self.get_color(score)

            start_point = (int(x), int(y))
            end_point = (int(x+w), int(y+h))

            cv.rectangle(image, start_point, end_point, color, self.config["thickness"])
            text = f"{label} ({score})"
            text_pos = (int(x), int(y) - self.config["margin"])

            cv.putText(
                image,
                text,
                text_pos,
                cv.FONT_HERSHEY_COMPLEX,
                self.config["font_scale"],
                color,
                self.config["thickness"]
            )
        return image