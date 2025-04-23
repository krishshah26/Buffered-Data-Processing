import pytest
from src.processor import process_event_stream

#Test Case 1
#Processes the first full batch of events (size defined by `buffer_size`)
def test_batch_processing():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]
    results = process_event_stream(events, buffer_size=3)
    assert len(results) == 1
    assert results[0]['avg_value'] == 20.0
    assert results[0]['max_value'] == 30.0
    assert results[0]['unique_users'] == 2

#Given Edge Cases
#Test Case 2
'''
1. What happens if `events` is empty?
If 'events' is empty 'process_event_stream' will return empty list[]
'''

def test_empty_events():
    events = []
    results = process_event_stream(events, buffer_size=3)
    assert results == []

#Test Case 3
'''
2. What if `buffer_size` is larger than the number of events?
If buffer_size is larger than the number of events, the batch remains incomplete and is not processed. The function returns an empty list []. 
'''

def test_larger_buffer_size():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}}
    ]
    results = process_event_stream(events, buffer_size=3)
    assert results == []

#Test Case 4 & 5
'''
3. How to handle invalid records (e.g., missing keys)?
a. The record with invalid missing keys will be considered as an invalid and so it will be ignored.
b. Non-numeric value: The record with non-numeric value will be ignored
'''

#a
def test_invalid_event_skipped():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},  
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z"},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]
    results = process_event_stream(events, buffer_size=3)
    assert len(results) == 1
    assert results[0]['unique_users'] == 3
    assert round(results[0]['avg_value'], 2) == 23.33
    assert results[0]['max_value'] == 40.0
    
#b
def test_non_numeric_value():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": "twenty", "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e4", "timestamp": "2025-04-01T10:00:03Z", "value": 40.0, "metadata": {"user_id": "u3"}},
    ]
    result = process_event_stream(events, buffer_size=3)
    assert len(result) == 1
    assert result[0]["avg_value"] == 30.0  
    assert result[0]["max_value"] == 40.0
    assert result[0]["unique_users"] == 3

#Test Case 6
'''
4. How does the function behave when `debug=True`?
If `debug` is True, the function prints each buffered event from a full batch.
The buffer is then cleared automatically via the generator logic.
'''

def test_debug_mode(capfd):
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u2"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
    ]
    process_event_stream(events, buffer_size=3, debug=True)
    out, _ = capfd.readouterr()
    assert "event_id" in out and "u2" in out

#Additional test cases

#Test Case 7
'''
5. All users are same.
Single user interacted multiple times
'''
def test_duplicate_users():
    events = [
        {"event_id": "e1", "timestamp": "2025-04-01T10:00:00Z", "value": 10.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e2", "timestamp": "2025-04-01T10:00:01Z", "value": 20.0, "metadata": {"user_id": "u1"}},
        {"event_id": "e3", "timestamp": "2025-04-01T10:00:02Z", "value": 30.0, "metadata": {"user_id": "u1"}},
    ]
    result = process_event_stream(events, buffer_size=3)
    assert len(result) == 1
    assert result[0]["avg_value"] == 20.0
    assert result[0]["max_value"] == 30.0
    assert result[0]["unique_users"] == 1

#Test Case 8
'''
6. Large version of events
To handle 10,000 events I have used buffer_size=100
'''

def test_large_batch():
    events = [
        {
            "event_id": f"e{i}",
            "timestamp": "2025-04-01T10:00:00Z",
            "value": float(i),
            "metadata": {"user_id": f"user{i % 50}"}
        }
        for i in range(10000)
    ]
    result = process_event_stream(events, buffer_size=100)
    assert len(result) == 100
    assert result[0]["max_value"] == 99.0
