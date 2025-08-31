// Basic WebSocket connection and state management
const ws = new WebSocket(`ws://${location.host}/ws`);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === 'state_update') {
        // Handle one-way data binding updates
        document.querySelectorAll(`[data-bind-text='${data.key}']`).forEach(el => {
            el.textContent = data.value;
        });
        // Handle two-way data binding updates for input values
        document.querySelectorAll(`[data-bind-value='${data.key}']`).forEach(el => {
            if (el.value !== data.value) {
                el.value = data.value;
            }
        });
        // Handle two-way data binding for checkbox checked status
         document.querySelectorAll(`[data-bind-checked='${data.key}']`).forEach(el => {
            if (el.checked !== data.value) {
                el.checked = data.value;
            }
        });
    }
};

window.winup = {
    sendEvent: (eventId, event) => {
        ws.send(JSON.stringify({ type: 'trigger_event', event_id: eventId }));
    },
    setState: (key, value) => {
        ws.send(JSON.stringify({ type: 'state_set', key: key, value: value }));
    }
};

// Two-way binding listeners
document.addEventListener('input', (event) => {
    const key = event.target.dataset.bindValue;
    if (key) {
        window.winup.setState(key, event.target.value);
    }
});
document.addEventListener('change', (event) => {
    if (event.target.type === 'checkbox') {
        const key = event.target.dataset.bindChecked;
        if (key) {
           window.winup.setState(key, event.target.checked);
        }
    }
});