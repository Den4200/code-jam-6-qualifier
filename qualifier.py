from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from timeit import timeit


def _parse_tz(dt: str, truncated: bool) -> Dict[str, Any]:
    """Parse ISO-8601 formatted time stamp for timezone"""

    offset = 0
    tz_ids = '+-Z'

    for id_ in tz_ids:
        if id_ in dt[-1]:
            tz = dt[-1].split(id_)
            sign = 1 if id_ == '+' else -1

            if truncated and id_ != 'Z':
                hours, mins = tz[1][:2], tz[1][2:]
                
            elif not truncated and id_ != 'Z':
                hm = tz[1].split(':')

                if len(hm) == 2:
                    hours, mins = hm
                else:
                    hours, mins = hm[0], ''

            elif id_ == 'Z':
                hours = mins = 0
                z_index = dt[-1].find('Z')

                if dt[-1][z_index:] != 'Z':
                    raise Exception("Nothing should be after 'Z'")

            mins = 0 if mins == '' else mins
            try:
                offset = (int(hours) + (int(mins) / 60)) * sign
            except ValueError as e:
                error = e.__str__()

                if error == "invalid literal for int() with base 10: ''":
                    raise ValueError(f"Added '{id_}' without offset") from None

                elif error.startswith('invalid literal for int() with base 10:'):
                    raise ValueError('Invalid integer value for timezone offset') from None

                else:
                    # In case an unknown value error appears
                    raise ValueError(error) from None
            
            try:
                return {
                    'timezone': timezone(timedelta(seconds=offset*60*60)),
                    'milisecs': tz[0]
                }
            except UnboundLocalError:
                raise Exception('Invalid format') from None

    # Return defaults if there is not timezone specified
    return {
        'timezone': None,
        'milisecs': dt[-1]
    }


def parse_iso8601(timestamp: str) -> datetime:
    """Parse an ISO-8601 formatted time stamp."""
    
    dt = None

    try:
        if timestamp[4] == '-' and timestamp[7] == '-':
            truncated = False

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
            truncated = True
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

    except IndexError as e:
        error = e.__str__()

        if error == 'string index out of range':
            raise Exception('Invalid date format') from None

        else:
            # In case an unknown value error appears
            raise IndexError(error) from None

    tzinfo = _parse_tz(dt, truncated)
    dt[-1] = tzinfo['milisecs']

    try:
        return datetime(*map(int, dt), tzinfo=tzinfo['timezone'])
    except ValueError as e:
        error = e.__str__()

        errors = {
            # Default error: Custom error
            'microsecond must be in 0..999999': 'Microseconds must be within the range of 0 - 999999',
            'second must be in 0..59': 'Seconds must be within the range of 0 - 59',
            'minute must be in 0..59': 'Minutes must be within the range of 0 - 59',
            'hour must be in 0..23': 'Hours must be within the range of 0 - 23',
            "invalid literal for int() with base 10: ''": "Added trailing 'T'/'-'/':'",
        }

        try:
            raise ValueError(errors[error]) from None
        except KeyError:

            if error.startswith('invalid literal for int() with base 10:'):
                raise ValueError('Invalid integer value for date/time') from None

            # In case an unknown value error appears
            raise ValueError(error) from None

    # Timestamp formatted incorrectly
    except UnboundLocalError:
        raise Exception('Invalid format') from None


time = timeit("parse_iso8601('2009-12-23T12:23:34.456789+04:00')", globals=globals(), number=100000)/1000
print(time)
