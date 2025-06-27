# Calendar

The `Calendar` widget provides a standard monthly calendar view, allowing users to select a date.

## Usage

```python
from winup import ui, winup

@winup.component
def CalendarExample():
    
    date_label = ui.Label(text="No date selected")

    def on_date_selection(date):
        # The date object is a QDate
        formatted_date = date.toString("yyyy-MM-dd")
        date_label.set_text(f"Selected: {formatted_date}")

    calendar = ui.Calendar()
    calendar.selectionChanged.connect(on_date_selection)

    return ui.Column(children=[
        calendar,
        date_label
    ])
```

## Constructor Parameters

The `Calendar` widget has no special constructor parameters beyond those inherited from `QCalendarWidget`.

## Methods

The `Calendar` inherits all methods from `QCalendarWidget`, including:

- `.selectedDate() -> QDate`: Returns the currently selected date as a `QDate` object.
- `.setSelectedDate(date: QDate)`: Programmatically sets the selected date.
- `.showToday()`: Selects the current date.

## Events

- `.selectionChanged`: A signal that is emitted whenever the user selects a new date. Connect a function to this signal to handle date selections.

## Styling

The `Calendar` widget comes with a significant amount of default styling to give it a modern look and feel. You can override these styles by passing a `props` dictionary with your own QSS properties, although it may require using complex Qt selectors to target specific parts of the calendar. 