
# 1. Buffered Data Processing

**Approach**

I designed the solution to process a stream of user events by grouping them into fixed-size batches using a helper generator function. While buffering, I validated that each event has the required fields and that the value is numeric; any incomplete or malformed records are skipped early on to avoid crashes or skewed metrics.

The process_event_stream function either computes metrics like average value, max value, and unique users when in normal mode, or prints raw events if debug=True. I made sure to handle edge cases like empty input, incomplete batches, and invalid data gracefully. 

**Core Components**

- batch_generator(events, buffer_size)
This function buffers incoming events into batches of a given size. It filters out any invalid or incomplete records (like missing fields or non-numeric values) before yielding a clean batch.

- process_event_stream(events, buffer_size=3, debug=False)
This function uses the generator to process each batch. In normal mode, it calculates metrics like average value, max value, and unique user count per batch. In debug mode, it simply prints each event to help with inspection or logging, without computing metrics.

These components are present in *processor.py* file.

**Test Cases Covered**

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

There are total 8 test cases for this question.

These test cases are present in *test_processor.py* file.

# 2. Buffered Data Processing

**Approach**

I approached this by first grouping each attendee with the unique set of years they attended the biennial conference. Using a defaultdict(set), I eliminated duplicate entries automatically.

Then for each attendee, I sorted their attendance years and calculated their longest streak of sessions spaced exactly two years apart — this is what defines a "consecutive streak" in this scenario.

After computing the streaks for all attendees, I identified the longest one. If only one person had that streak, I returned their name; if there was a tie, I returned all top names in alphabetical order.

**Core Components**

- find_top_attendee(meetings)

This function is designed to analyze a list of attendees and the years they participated in a biennial conference. It first groups each person’s attendance using a defaultdict(set) to ensure years are unique and easy to work with. For each attendee, their years are sorted so the function can identify streaks where attendance occurred exactly two years apart. It then calculates the longest such streak for each person. After all streaks are computed, the function returns the attendee with the longest streak. If there’s a tie, it returns all top performers in a sorted list.

This function is present in *meeting_analysis.py* file.

**Test Cases Covered**

| Test Case              | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| Longest Streak         | Returns the attendee with the longest consecutive biennial streak           |
| Tie Between Attendees  | Returns a sorted list of names if multiple attendees share the top streak   |
| Empty Input            | Handles an empty meeting list gracefully                                    |
| Single Attendee        | Works correctly with only one attendee                                      |
| Non-consecutive Years  | Correctly resets streaks if the 2-year interval is broken                   |
| Duplicate Entries      | Ignores repeated person-year pairs using a set    

There are total 6 test cases for this question.

These test cases are present in *test_meeting_analysis.py* file.

# Running Test Cases

There are total 14 test cases considering both the files.

Step 1:
```bash
pip install pytest
```
Step 2:
```bash
PYTHONPATH=./ pytest
```

Expected Output: 14 passed
