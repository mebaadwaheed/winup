# Image

The `Image` component renders an HTML `<img>` tag, used for displaying images.

## Usage

```python
from winup import web

@web.component
def ImageGallery():
    return web.ui.Row(gap="10px", children=[
        # Image from an external URL
        web.ui.Image(
            src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png",
            alt="Python Logo",
            style={'width': '150px'}
        ),
        
        # Image from a local static path
        # (Assumes you have a static directory configured to serve images)
        web.ui.Image(
            src="/static/images/my_avatar.jpg",
            alt="My Avatar",
            style={'width': '100px', 'border_radius': '50%'}
        )
    ])
```

## Arguments
- `src` (str): The URL or path to the image source.
- `alt` (str): The alternative text for the image, which is important for accessibility.
- `props` (dict, optional): A dictionary of additional HTML attributes.
- `**kwargs`: Keyword arguments are also treated as HTML attributes. 