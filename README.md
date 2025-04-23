## Core Components

### `batch_generator(events, buffer_size)`

- Iterates through incoming events
- Validates required fields: `event_id`, `timestamp`, `metadata['user_id']`, and `value`
- Skips events with missing keys or non-numeric `value`
- Yields a batch once the buffer reaches the specified `buffer_size`

### `process_event_stream(events, buffer_size=3, debug=False)`

- Consumes batches from `batch_generator`
- In debug mode: prints each event in the batch
- In standard mode: computes average value, maximum value, and unique user count
- Skips batches with no valid numeric values

## Test Cases Covered

| Test Case         | Description                                    |
| ----------------- | ---------------------------------------------- |
| Valid Batch       | Processes a complete batch of valid events     |
| Empty Input       | Handles an empty list gracefully               |
| Oversized Buffer  | Skips processing when the batch is incomplete  |
| Missing Keys      | Skips events with missing or invalid structure |
| Non-numeric Value | Filters out non-numeric values                 |
| Debug Mode        | Prints events instead of computing metrics     |
| Duplicate Users   | Validates unique user count                    |
| Large Dataset     | Handles 10,000 events with batching            |

## Running Tests

Ensure `pytest` is installed, then run:

```bash
pip install pytest
PYTHONPATH=./ pytest

## Folder Structure

Buffered-Data-Processing/ ├── src/ │ └── processor.py # Core processing logic ├── tests/ │ └── test_processor.py # Unit tests for batching and edge cases ├── README.md # Project documentation ├── requirements.txt # Python package dependencies ├── .gitignore # Files/folders excluded from version control

## Files Ignored by Git
__pycache__/
.pytest_cache/
*.pyc

```

# Meeting Scheduling Analysis

This module solves a classic data problem: given a list of attendees and the years they attended a biennial conference (held every two years), identify who has the longest streak of consecutive attendance.

---

## Objective

To find the attendee (or attendees) with the longest streak of back-to-back conference appearances, spaced exactly two years apart. If multiple people have the same longest streak, all names are returned alphabetically.

---

## Features

- Handles duplicate entries automatically
- Calculates exact 2-year interval streaks (e.g., 2000 → 2002 → 2004)
- Returns either a single name or a sorted list
- Covers edge cases like empty input or non-consecutive years

---

## Function

```python
find_top_attendee(meetings: List[Tuple[str, int]]) -> Union[str, List[str]]
