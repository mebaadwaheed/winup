# Carousel

The `Carousel` is a widget that displays a collection of "slides" (other widgets) one at a time, with a smooth cross-fade animation and navigation controls. It's perfect for onboarding flows, image galleries, or featured content sections.

## Usage

```python
from winup import ui, winup

@winup.component
def CarouselExample():
    # Define the slides for the carousel
    slide1 = ui.Label("Welcome to the Carousel!", props={"font-size": "24px", "alignment": "AlignCenter"})
    slide2 = ui.Image(src="path/to/image.png")
    slide3 = ui.Column(children=[
        ui.Label("Final Slide"),
        ui.Button("Get Started")
    ])

    return ui.Carousel(
        children=[slide1, slide2, slide3],
        autoplay_ms=3000, # Switch slides every 3 seconds
        animation_duration=500 # 0.5 second fade animation
    )
```

## Constructor Parameters

- `children: list` (optional): A list of widgets to be used as the slides.
- `animation_duration: int`: The duration of the cross-fade animation in milliseconds. Defaults to `400`.
- `autoplay_ms: int`: If greater than `0`, the carousel will automatically advance to the next slide after this many milliseconds. Defaults to `0` (disabled). User interaction will pause autoplay.
- `show_nav_buttons: bool`: If `True`, shows the "<" and ">" navigation buttons. Defaults to `True`.
- `show_indicators: bool`: If `True`, shows the dot indicators at the bottom. Defaults to `True`.
- `nav_button_props: dict` (optional): A dictionary of style props to apply to the navigation buttons.
- `indicator_props: dict` (optional): A dictionary of style props to apply to the indicator dots.

## Methods

### `.add_slide(widget: QWidget)`
Adds a new widget to the end of the carousel.

### `.go_to(index: int)`
Navigates to the slide at the specified index.

### `.show_next()`
Navigates to the next slide in the sequence (wraps around).

### `.show_previous()`
Navigates to the previous slide in the sequence (wraps around).

### `.set_autoplay(msecs: int)`
Changes the autoplay interval. Set to `0` to disable autoplay.

### `.set_animation_duration(msecs: int)`
Changes the animation duration.

### `.count() -> int`
Returns the total number of slides.

## Events

### `.slideChanged`
A Qt Signal that is emitted whenever the visible slide changes. It sends the index of the new slide as an argument.

```python
def on_slide_change(new_index):
    print(f"Moved to slide {new_index}")

my_carousel = ui.Carousel(...)
my_carousel.slideChanged.connect(on_slide_change)
``` 