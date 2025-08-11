# Tailwind Styling Guide

This document explains how to use the Tailwind CSS-like styling feature in your WinUp application.

## Usage

You can apply Tailwind styles to any UI component by passing a `tailwind` string to its `props` dictionary.

### Desktop Components

For desktop components, the `tailwind` classes are transpiled to PySide6 QSS.

**Example:**

```python
import winup.ui as ui

ui.Button("Click Me", props={'tailwind': 'bg-blue-500 text-white p-4'})
```

### Web Components

For web components, the `tailwind` classes are transpiled to standard CSS.

**Example:**

```python
import winup.web.ui as web_ui

web_ui.Button("Click Me", props={'tailwind': 'bg-blue-500 text-white p-4'})
```

## Available Classes

Here is a list of all available Tailwind classes and their corresponding output for both web and desktop platforms.

| Tailwind Class | Desktop (QSS) | Web (CSS) |
| --- | --- | --- |
| `bg-blue-500` | `background-color: #3B82F6;` | `background-color: #3B82F6;` |
| `text-black` | `color: #000000;` | `color: #000000;` |
| `text-white` | `color: #FFFFFF;` | `color: #FFFFFF;` |
| `p-4` | `padding: 16px;` | `padding: 1rem;` |
| `p-2` | `padding: 8px;` | `padding: 0.5rem;` |
| `p-1` | `padding: 4px;` | `padding: 0.25rem;` |
| `p-0` | `padding: 0px;` | `padding: 0rem;` |
| `m-4` | `margin: 16px;` | `margin: 1rem;` |
| `m-2` | `margin: 8px;` | `margin: 0.5rem;` |
| `m-1` | `margin: 4px;` | `margin: 0.25rem;` |
| `m-0` | `margin: 0px;` | `margin: 0rem;` |
| `w-1/2` | `width: 50%;` | `width: 50%;` |
