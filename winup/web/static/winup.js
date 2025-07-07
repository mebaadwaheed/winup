// winup/web/static/winup.js

(function() {
    'use strict';

    let socket;

    // Make the event sender globally available
    window.winup = {
        sendEvent: (eventId, event) => {
            // In the future, we could serialize parts of the event object
            // For now, we just send the ID.
            sendMessage({
                type: 'trigger_event',
                event_id: eventId,
            });
        }
    };

    function connect() {
        // Use wss:// if the page is loaded over https://
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/ws`;

        socket = new WebSocket(wsUrl);

        socket.onopen = function(event) {
            console.log("WinUp WebSocket connection established.");
        };

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            if (data.type === 'state_update') {
                updateBoundElements(data.key, data.value);
            }
        };

        socket.onclose = function(event) {
            console.log("WinUp WebSocket connection closed. Attempting to reconnect...");
            // Simple reconnect logic
            setTimeout(connect, 3000);
        };
        
        socket.onerror = function(error) {
            console.error("WebSocket Error: ", error);
        };
    }

    function updateBoundElements(key, value) {
        // --- Text binding ---
        const textElements = document.querySelectorAll(`[data-bind-text='${key}']`);
        textElements.forEach(el => el.textContent = value);

        // --- Value binding (for inputs) ---
        const valueElements = document.querySelectorAll(`[data-bind-value='${key}']`);
        valueElements.forEach(el => {
            if (document.activeElement !== el) {
                el.value = value;
            }
        });

        // --- Checkbox binding ---
        const checkboxElements = document.querySelectorAll(`[data-bind-checked='${key}']`);
        checkboxElements.forEach(el => {
            el.checked = !!value; // Ensure the value is a boolean
        });
    }

    function sendMessage(data) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(data));
        } else {
            console.error("Cannot send message, WebSocket is not open.");
        }
    }

    /**
     * Sets up listeners for two-way data binding on input and change events.
     */
    function setupTwoWayBinding() {
        document.body.addEventListener('input', event => {
            const target = event.target;
            if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA') {
                const bindKey = target.getAttribute('data-bind-value');
                if (bindKey) {
                    sendMessage({
                        type: 'state_set',
                        key: bindKey,
                        value: target.value
                    });
                }
            }
        });

        document.body.addEventListener('change', event => {
            const target = event.target;
            if (target.type === 'checkbox') {
                const bindKey = target.getAttribute('data-bind-checked');
                if (bindKey) {
                    sendMessage({
                        type: 'state_set',
                        key: bindKey,
                        value: target.checked
                    });
                }
            }
        });
    }

    // Connect on DOM ready
    document.addEventListener('DOMContentLoaded', () => {
        connect();
        setupTwoWayBinding();
    });

})(); 