# Image

The `Image` widget is used to display images. It can load images from both local file paths and remote URLs.

## Usage

```python
from winup import ui, winup

@winup.component
def ImageExample():
    return ui.Column(children=[
        ui.Label(text="Image from a local file:"),
        ui.Image(src="path/to/my-local-image.png"),

        ui.Label(text="Image from a URL, scaled to width:"),
        ui.Image(
            src="https://via.placeholder.com/300",
            scale_to_width=150
        ),

        ui.Label(text="Stretched image (aspect ratio ignored):"),
        ui.Image(
            src="path/to/another-image.jpg",
            scale_to_height=100,
            keep_aspect_ratio=False
        )
    ])
```

## How it Works

- **Local Files:** If the `src` path does not start with `http`, the widget loads it directly from the local filesystem.
- **Remote URLs:** If the `src` path starts with `http`, the widget uses a background network loader to download the image asynchronously. The image will appear once the download is complete.

## Constructor Parameters

- `src: str`: The path to the image. This can be a local file path (e.g., `"assets/logo.png"`) or a remote URL (e.g., `"https://.../image.jpg"`).
- `scale_to_width: int` (optional): If provided, the image will be scaled to this width in pixels.
- `scale_to_height: int` (optional): If provided, the image will be scaled to this height in pixels.
- `keep_aspect_ratio: bool`: If `True` (the default), the image's aspect ratio will be maintained during scaling. If `False`, the image may be stretched to fit the specified dimensions. 