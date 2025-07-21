from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from ...core.network import ImageLoader

class Image(QLabel):
    """A widget to display images from files or URLs."""

    def __init__(self, src: str, scale_to_width: int = None, scale_to_height: int = None, keep_aspect_ratio: bool = True, parent=None):
        super().__init__(parent)
        self.src = src
        self.scale_to_width = scale_to_width
        self.scale_to_height = scale_to_height
        self.keep_aspect_ratio = keep_aspect_ratio
        self._pixmap = None  # To hold a reference to the pixmap
        
        if src.startswith('http'):
            self.loader = ImageLoader(self)
            self.loader.finished.connect(self._on_image_loaded)
            self.loader.load_from_url(src)
        else:
            self._pixmap = QPixmap(src)
            self.set_pixmap(self._pixmap)

    def _on_image_loaded(self, pixmap: QPixmap):
        self._pixmap = pixmap
        """Callback for when the image is downloaded."""
        self.set_pixmap(pixmap)

    def set_pixmap(self, pixmap: QPixmap):
        """Sets the pixmap with the stored scaling options."""
        if not pixmap or pixmap.isNull():
            return

        aspect_mode = Qt.KeepAspectRatio if self.keep_aspect_ratio else Qt.IgnoreAspectRatio
        
        scaled_pixmap = pixmap
        if self.scale_to_width:
            scaled_pixmap = pixmap.scaledToWidth(self.scale_to_width, mode=aspect_mode)
        elif self.scale_to_height:
            scaled_pixmap = pixmap.scaledToHeight(self.scale_to_height, mode=aspect_mode)
            
        super().setPixmap(scaled_pixmap)