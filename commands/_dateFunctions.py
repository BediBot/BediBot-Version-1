import datetime
import re


def check_for_errors_in_date(year, month, day):
    # return values: 0 is no errors, 1 is invalid syntax, 2 is invalid date

    if not re.match('^\d{4}', year) and re.match('^\d{2}', month) and re.match('^\d{2}', day):
        return 1
    else:
        try:
            datetime.datetime(int(year), int(month), int(day))
        except ValueError:
            return 2
        return 0
