# How WinUp for Web Works

WinUp's web framework is designed to let you build interactive, stateful web user interfaces using pure Python. It combines a Python backend server (FastAPI) with a lightweight JavaScript frontend to create a seamless development experience.

## Core Concepts

1.  **Python-Centric Components**: You write your UI components as Python functions or classes. You don't need to write HTML, CSS, or JavaScript directly. WinUp components map directly to HTML elements.

2.  **Declarative UI**: You declare what your UI should look like based on the current application state. You compose simple components (like `Label`, `Button`, `Row`, `Column`) into complex user interfaces.

3.  **Server-Side Rendering (SSR)**: When you navigate to a URL, the Python server renders the appropriate component tree into a string of HTML and sends it to the browser. This ensures fast initial page loads and good SEO.

4.  **State Management & Reactivity**:
    - The application state (e.g., a counter, user input, a list of items) lives on the server.
    - You use `web.state.create()` to create reactive state variables.
    - When you bind a component's property (like a `Label`'s text) to a state variable, WinUp establishes a link.
    - When the state variable is updated on the server (e.g., through an `@web.tasks.run` background task or an `on_click` event), the server automatically sends the new value to the browser over a persistent WebSocket connection.

5.  **Client-Side Updates**: A small, generic JavaScript file (`winup.js`) runs in the browser. Its jobs are:
    - To listen for state updates from the server via WebSocket.
    - To update the specific parts of the DOM that are bound to that state (e.g., changing the text of a label, updating the value of an input).
    - To send user events (like button clicks or text input) back to the server to trigger Python event handlers.

## The Request/Response Flow

Here's a typical flow of events:

1.  **Initial Load**:
    - Browser requests a URL (e.g., `/`).
    - The FastAPI server matches the URL to a route and calls the corresponding Python component function (e.g., `HomePage()`).
    - The component function and its children are rendered to an HTML string.
    - The server injects this HTML into a base template (`index.html`) and sends the full page to the browser.
    - The browser also loads `winup.js` and establishes a WebSocket connection back to the server.

2.  **User Interaction**:
    - User clicks a `Button` component.
    - The `on_click` event is sent over the WebSocket to the server, identifying the specific handler function to run.
    - The Python event handler function (e.g., `increment_counter`) is executed.

3.  **State Update**:
    - The event handler modifies a state variable (e.g., `await counter.set(1)`).
    - The `StateManager` on the server broadcasts a message over the WebSocket to all connected clients: `{"type": "state_update", "key": "counter", "value": 1}`.

4.  **DOM Patching**:
    - The `winup.js` library on the client receives the message.
    - It finds all HTML elements with the `data-bind-text="counter"` attribute.
    - It updates the `textContent` of those elements to `1`.

This architecture allows you to write your entire application logic in Python, with WinUp handling the complex communication between the server and the browser. 