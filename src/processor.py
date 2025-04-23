"""
This function generates batches of validated events from an event stream.
Skips events with missing keys or non-numeric 'value' fields.
Yields batches once the specified buffer_size is met.
"""
def batch_generator(events, buffer_size):
    buffer = []
    for event in events:
        try:
            value = event['value']
            _ = event['event_id']
            _ = event['timestamp']
            _ = event['metadata']['user_id']
            if not isinstance(value, (int, float)):
                continue 
        except (KeyError, TypeError):
            continue
        buffer.append(event)
        if len(buffer) == buffer_size:
            yield buffer
            buffer = []

'''
This function processes incoming event batches to compute metrics or print debug data.
In non-debug mode, calculates average value, max value, and unique user count per batch.
In debug mode, prints raw events instead of processing them.
'''
def process_event_stream(events, buffer_size=3, debug=False):
    if not isinstance(events, list) or buffer_size <= 0:
        raise ValueError("Invalid input: events must be a list and buffer_size must be > 0")

    results = []
    for batch in batch_generator(events, buffer_size):
        if debug:
            for event in batch:
                print(event)
        else:
            values = [e['value'] for e in batch if isinstance(e['value'], (int, float))]
            if not values:
                continue 
            users = {e['metadata']['user_id'] for e in batch}
            results.append({
                'avg_value': sum(values) / len(values),
                'max_value': max(values),
                'unique_users': len(users)
            })

    return results
