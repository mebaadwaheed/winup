# Camera Tool

The `winup.tools.camera.Camera` class makes it easy to capture images from the system's webcam. It requires `opencv-python` and `numpy`.

```python
import winup
from winup import ui
from winup.tools.camera import Camera

@winup.component
def CameraView():
    # Create a label to display the camera feed
    image_label = ui.Label()

    def capture_and_display():
        try:
            # Initialize the camera
            cam = Camera() 
            
            # Capture a single frame
            pixmap = cam.capture_frame() # Returns a QPixmap
            
            if pixmap:
                # Display the captured frame in the label
                image_label.set_pixmap(pixmap)
            
            # Clean up the camera resource
            cam.release()
        except IOError as e:
            image_label.set_text(f"Error: {e}")

    return ui.Column(children=[
        image_label,
        ui.Button("Capture Frame", on_click=capture_and_display)
    ])

# To run this, you would need a WinUp app instance.
# Example: winup.run(main_component_path="camera_demo:CameraView", title="Camera Demo")
```