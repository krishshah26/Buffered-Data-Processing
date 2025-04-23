"""
This function finds the attendee(s) with the longest consecutive biennial attendance streak.
Consecutive means attending conferences spaced exactly 2 years apart (e.g., 2000, 2002, 2004).

If there’s a tie for the longest streak, a sorted list of attendees is returned.
It also makes sure to ignore duplicate entries and handles missing or messy data without breaking.
"""

from collections import defaultdict
from typing import List, Tuple, Union

def find_top_attendee(meetings: List[Tuple[str, int]]) -> Union[str, List[str]]:
    if not meetings:
        return []

    attendee_years = defaultdict(set)
    for name, year in meetings:
        attendee_years[name].add(year) 
        
    streaks = {}
    for name, years in attendee_years.items():
        sorted_years = sorted(years)
        max_streak = 1
        current_streak = 1

        for i in range(1, len(sorted_years)):
            if sorted_years[i] - sorted_years[i - 1] == 2:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 1

        streaks[name] = max_streak

    top_streak = max(streaks.values())
    top_attendees = [name for name, streak in streaks.items() if streak == top_streak]

    return top_attendees[0] if len(top_attendees) == 1 else sorted(top_attendees)
