from PySide6.QtCore import (
    QParallelAnimationGroup,
    QPropertyAnimation,
    QTimer,
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QFrame,
    QGraphicsOpacityEffect,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from winup import style

# No longer using fx for the carousel transition to allow for a cross-fade.
# from winup.animate import fx

class Carousel(QWidget):
    """
    A widget that displays a collection of widgets in a "carousel" style,
    one at a time, with a smooth cross-fade animation and navigation controls.
    """

    slideChanged = Signal(int)

    def __init__(
        self,
        parent: QWidget = None,
        children: list = None,
        props: dict = None,
        animation_duration: int = 400,
        autoplay_ms: int = 0,
        show_nav_buttons: bool = True,
        show_indicators: bool = True,
        nav_button_props: dict = None,
        indicator_props: dict = None,
    ):
        super().__init__(parent)
        self._slides = []
        self._currentIndex = -1
        self._animation_duration = animation_duration
        self._is_animating = False
        self._nav_button_props = nav_button_props or {}
        self._indicator_props = indicator_props or {}

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Slide Area - A container with a grid layout for robust stacking and resizing
        self.slide_container = QFrame()
        self.slide_container.setMinimumSize(1, 150)
        self.slide_layout = QGridLayout(self.slide_container)
        self.slide_layout.setContentsMargins(0, 0, 0, 0)
        self.slide_layout.setSpacing(0)
        self.main_layout.addWidget(self.slide_container, 1)

        # Navigation Controls
        self.nav_frame = QFrame()
        self.nav_layout = QHBoxLayout(self.nav_frame)
        self.nav_layout.setContentsMargins(0, 5, 0, 5)

        self.prev_button = QPushButton("<")
        self.prev_button.setProperty("class", "carousel-nav-button")
        self.next_button = QPushButton(">")
        self.next_button.setProperty("class", "carousel-nav-button")
        
        style.styler.apply_props(self.prev_button, self._nav_button_props)
        style.styler.apply_props(self.next_button, self._nav_button_props)

        self.indicator_layout = QHBoxLayout()
        self.indicator_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.nav_layout.addWidget(self.prev_button)
        self.nav_layout.addStretch()
        self.nav_layout.addLayout(self.indicator_layout)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_button)
        self.main_layout.addWidget(self.nav_frame)

        # Hide controls if requested
        if not show_nav_buttons:
            self.prev_button.hide()
            self.next_button.hide()
        if not show_indicators:
            self.indicator_layout.hide()

        # Connections
        self.prev_button.clicked.connect(self.show_previous)
        self.next_button.clicked.connect(self.show_next)

        # Autoplay
        self.autoplay_timer = QTimer(self)
        self.autoplay_timer.timeout.connect(self.show_next)
        if autoplay_ms > 0:
            self.set_autoplay(autoplay_ms)

        # Add initial slides if provided
        if children:
            for child in children:
                self.add_slide(child)

        # Store props for web conversion
        self.props = props

    def add_slide(self, widget: QWidget):
        """Adds a widget as a new slide in the carousel."""
        # Ensure the slide has an opacity effect for animation.
        if not widget.graphicsEffect():
            widget.setGraphicsEffect(QGraphicsOpacityEffect(widget))

        # Add to the layout. The layout now handles parenting and geometry.
        self.slide_layout.addWidget(widget, 0, 0)

        is_first_slide = len(self._slides) == 0
        self._slides.append(widget)
        self._add_indicator()

        if is_first_slide:
            self._currentIndex = 0
            widget.show()
            self._update_indicators()
        else:
            widget.hide()  # Hide all non-active slides

    def _add_indicator(self):
        indicator = QPushButton()
        indicator.setCheckable(True)
        indicator.setProperty("class", "carousel-indicator")
        indicator.setFixedSize(10, 10)
        
        # Apply custom styles
        style.styler.apply_props(indicator, self._indicator_props)

        indicator_index = len(self._slides) - 1
        indicator.clicked.connect(lambda: self.go_to(indicator_index))
        self.indicator_layout.addWidget(indicator)

    def _update_indicators(self):
        for i in range(len(self._slides)):
            indicator = self.indicator_layout.itemAt(i).widget()
            indicator.setChecked(i == self._currentIndex)

        has_multiple_slides = len(self._slides) > 1
        self.prev_button.setEnabled(has_multiple_slides)
        self.next_button.setEnabled(has_multiple_slides)

    def go_to(self, index: int):
        """Navigates to the specified slide index with a cross-fade animation."""
        if (
            index == self._currentIndex
            or index < 0
            or index >= len(self._slides)
            or self._is_animating
            or len(self._slides) < 2
        ):
            return

        # Stop autoplay if user interacts
        if self.autoplay_timer.isActive():
            self.autoplay_timer.stop()

        self._is_animating = True

        current_widget = self._slides[self._currentIndex]
        self._currentIndex = index
        next_widget = self._slides[self._currentIndex]

        self._update_indicators()

        # --- Cross-fade Animation ---
        next_widget.graphicsEffect().setOpacity(0.0)
        next_widget.show()
        next_widget.raise_()  # Ensure the new slide is visually on top

        anim_group = QParallelAnimationGroup(self)

        anim_out = QPropertyAnimation(current_widget.graphicsEffect(), b"opacity")
        anim_out.setDuration(self._animation_duration)
        anim_out.setEndValue(0.0)
        anim_group.addAnimation(anim_out)

        anim_in = QPropertyAnimation(next_widget.graphicsEffect(), b"opacity")
        anim_in.setDuration(self._animation_duration)
        anim_in.setEndValue(1.0)
        anim_group.addAnimation(anim_in)

        def on_animation_finish():
            current_widget.hide()
            current_widget.graphicsEffect().setOpacity(1.0) # Reset for next time
            self._is_animating = False
            self.slideChanged.emit(self._currentIndex)
            # Restart autoplay if it was active before
            if self.autoplay_timer.interval() > 0:
                self.autoplay_timer.start()

        anim_group.finished.connect(on_animation_finish)
        anim_group.start(QPropertyAnimation.DeletionPolicy.DeleteWhenStopped)

    def show_next(self):
        count = len(self._slides)
        if count > 0:
            self.go_to((self._currentIndex + 1) % count)

    def show_previous(self):
        count = len(self._slides)
        if count > 0:
            self.go_to((self._currentIndex - 1 + count) % count)

    def set_autoplay(self, msecs: int):
        """Enables or disables autoplay."""
        if self.autoplay_timer.isActive():
            self.autoplay_timer.stop()
        
        if msecs > 0:
            self.autoplay_timer.setInterval(msecs)
            self.autoplay_timer.start()
        else:
             self.autoplay_timer.setInterval(0)

    def set_animation_duration(self, msecs: int):
        self._animation_duration = msecs

    def count(self):
        return len(self._slides)
    
    def resizeEvent(self, event):
        """Ensure slides are resized when the carousel is resized."""
        super().resizeEvent(event)
        for slide in self._slides:
            slide.resize(self.slide_container.size()) 