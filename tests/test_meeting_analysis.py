import pytest
from src.meeting_analysis import find_top_attendee


#Test Case 1
'''
1. Returns the name of the attendee with the maximum streak length.
'''

def test_case_1():
    meetings = [
        ("Alice", 2000), ("Alice", 2002), ("Alice", 2004),
        ("Bob", 2000), ("Bob", 2002),
        ("Charlie", 2000), ("Charlie", 2002), ("Charlie", 2004), ("Charlie", 2006),
    ]
    assert find_top_attendee(meetings) == "Charlie"

#Test Case 2
'''
2. In case of a tie, returns a list of names sorted alphabetically.
'''

def test_case_2():
    meetings = [
        ("Alice", 2000), ("Alice", 2002),
        ("Bob", 2000), ("Bob", 2002),
    ]
    assert find_top_attendee(meetings) == ["Alice", "Bob"]

#Given Edge Cases
#Test Case 3
'''
3. Empty meeting list.
If meeting list is empty then the function will return empty list[].
'''
def test_empty_list():
    assert find_top_attendee([]) == []

#Test Case 4
'''
4. Single attendee.
'''
def test_single_attendee():
    meetings = [("Alice", 2000), ("Alice", 2002), ("Alice", 2004)]
    assert find_top_attendee(meetings) == "Alice"

#Test Case 5
'''
5. Non-consecutive years in data.
Considering attendees attending sessions exactly 2 years apart.
'''
def test_non_consecutive_years():
    meetings = [
        ("Alice", 2000), ("Alice", 2003), ("Alice", 2006),
        ("Bob", 2000), ("Bob", 2002), ("Bob", 2004),
    ]
    assert find_top_attendee(meetings) == "Bob"

#Test Case 6
'''
6. Duplicate entries for the same person-year.
Duplicate entries are ignored.
'''
def test_duplicate_entries():
    meetings = [
        ("Alice", 2000), ("Alice", 2000), ("Alice", 2002), ("Alice", 2002),
        ("Bob", 2000), ("Bob", 2002),
    ]
    assert find_top_attendee(meetings) == ["Alice", "Bob"]
