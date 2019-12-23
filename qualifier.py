import datetime
from typing import List
import re


def parse_iso8601(timestamp: str) -> datetime.datetime:
    """Parse an ISO-8601 formatted time stamp."""
    
    dt = None

    if timestamp[4] == '-' and timestamp[7] == '-':
        
        if 'T' in timestamp:
            ts = timestamp.split('T')
            mil = ts[1].split('.')

            if '.' in timestamp:
                dt = ts[0].split('-') + mil[0].split(':') + [mil[1]]
            else:
                dt = ts[0].split('-') + ts[1].split(':')

        else:
            dt = timestamp.split('-')

    elif timestamp[4] != '-' and timestamp[7] != '-':
        dt = [timestamp[:4], timestamp[4:6], timestamp[6:8]]

        if 'T' in timestamp:
            ts = timestamp.split('T')
            mil = ts[1].split('.')

            dt_temp = [mil[0][:2], mil[0][2:4], mil[0][4:]]

            if dt_temp[0] == '':
                raise ValueError("Added 'T' without time")

            dt += [time for time in dt_temp if time != '']

            if '.' in ts[1]:
                dt += [mil[1]]

    else:
        raise Exception('Invalid format: Missing/misplaced dashes')

    try:
        return datetime.datetime(*map(int, dt))
    except ValueError as e:
        error = e.__str__()

        errors = {
            'microsecond must be in 0..999999': 'Microseconds must be within the range of 0 - 999999',
            'second must be in 0..59': 'Seconds must be within the range of 0 - 59',
            'minute must be in 0..59': 'Minutes must be within the range of 0 - 59',
            'hour must be in 0..23': 'Hours must be within the range of 0 - 23',
            "invalid literal for int() with base 10: ''": "Added 'T' without time",
        }

        raise ValueError(errors[error]) from None

dt = '2009-12-23T12:34:56.789012'

print(parse_iso8601(dt))

