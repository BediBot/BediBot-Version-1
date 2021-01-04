import datetime
import re


def check_for_errors_in_date(year: int, month: int, day: int) -> int:
    # Return Values: 0 (No errors), 1 (Syntax Error), 2 (Date Error)

    if not (re.match('^\d{4}', year) and re.match('^\d{2}', month) and re.match('^\d{2}', day)):
        return 1
    else:
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return 2
        return 0
