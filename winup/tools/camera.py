import cv2
from PySide6.QtGui import QImage, QPixmap
import numpy as np

class Camera:
    """A utility for interacting with system cameras."""
    def __init__(self, camera_index=0):
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise IOError(f"Cannot open camera at index {camera_index}")

    def capture_frame(self, as_pixmap: bool = True):
        """
        Captures a single frame from the camera.

        Args:
            as_pixmap (bool): If True, returns a QPixmap. Otherwise, returns a raw numpy array (BGR).

        Returns:
            QPixmap or numpy.ndarray or None: The captured frame, or None if the capture failed.
        """
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        if as_pixmap:
            # Convert the captured frame from BGR to RGB
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            return QPixmap.fromImage(qt_image)
        
        return frame

    def release(self):
        """Releases the camera resource."""
        self.cap.release()

    def __del__(self):
        self.release()

# Example Usage (can be run directly)
if __name__ == '__main__':
    try:
        cam = Camera()
        pixmap = cam.capture_frame()
        if pixmap:
            # To display this, you would need a QApplication and a QLabel
            print("Frame captured successfully. To view it, display the returned QPixmap in a QLabel.")
            # For demonstration, let's save it.
            pixmap.save("camera_capture.png")
            print("Saved capture to camera_capture.png")
        else:
            print("Failed to capture frame.")
        cam.release()
    except IOError as e:
        print(e) 