import cv2

class Camera:
    def __init__(self):
        # Abrir câmera
        self.cap = cv2.VideoCapture(0)

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        return frame

    def get_small_frame(self):
        return cv2.resize(self.get_frame(), (0, 0), fx=0.25, fy=0.25)

    def get_jpg_frame(self):
        ret, frame = self.cap.read()

        if ret:
            ret, jpeg = cv2.imencode('.jpg', frame)

            return jpeg.tobytes()
        else:
            return None