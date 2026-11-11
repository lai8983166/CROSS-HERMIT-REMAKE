"""Bounded read-only receipt polling; never resubmit a guest mutation."""
import time
from devtools.isolated_vm_bounded_query_v3 import completed


def poll(query, matches, seconds, clock=time.monotonic, sleep=time.sleep):
    start = clock()
    rows = []
    for attempt in range(12):
        if clock() - start >= seconds:
            break
        response = query(attempt)
        rows.append(response)
        if clock() - start >= seconds:
            break
        if completed(response):
            value = response['response']['value']
            if matches(value):
                return response, rows
            if value.get('file_present') is not False:
                break
        else:
            break
        sleep(min(2, max(0, seconds - (clock()-start))))
    raise ValueError('durable receipt not confirmed within read-only budget')
