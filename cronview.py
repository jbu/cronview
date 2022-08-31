import sys


# from crontab(5):
# Each line has five time and date fields, followed by a user name
# (with optional ``:<group>'' and ``/<login-class>'' suffixes) if this is the system
# crontab file, followed by a command.  Commands are executed by cron(8) when the minute,
# hour, and month of year fields match the current time, and when at least one of the two
# day fields (day of month, or day of week) matches the current time (see ``Note'' below).
# cron(8) examines cron entries once every minute.  The time and date fields are:

#       field         allowed values
#       -----         --------------
#       minute        0-59
#       hour          0-23
#       day of month  1-31
#       month         1-12 (or names, see below)
#       day of week   0-7 (0 or 7 is Sun, or use names)

# A field may be an asterisk (*), which always stands for ``first-last''.

# Ranges of numbers are allowed.  Ranges are two numbers separated with a hyphen.  The
# specified range is inclusive.  For example, 8-11 for an ``hours'' entry specifies
# execution at hours 8, 9, 10 and 11.

# Lists are allowed.  A list is a set of numbers (or ranges) separated by commas.
# Examples: ``1,2,5,9'', ``0-4,8-12''.

# Step values can be used in conjunction with ranges.  Following a range with ``/<number>''
# specifies skips of the number's value through the range.  For example, ``0-23/2'' can be
# used in the hours field to specify command execution every other hour (the alternative in
# the V7 standard is ``0,2,4,6,8,10,12,14,16,18,20,22'').  Steps are also permitted after
# an asterisk, so if you want to say ``every two hours'', just use ``*/2''.

# Names can also be used for the ``month'' and ``day of week'' fields.  Use the first three
# letters of the particular day or month (case does not matter).  Ranges or lists of names
# are not allowed.


def generage_range(
    range_str: str, limits: tuple[int, int], name_substs: dict[str, int]
) -> set[int]:
    """
    Expand a range. As per crontab spec, there can be a variety of types of ranges,
    and they may also have step values.
    """
    # Sort out step values
    step_value = 1
    if "/" in range_str:
        range_str, step_value_str = range_str.split("/")
        try:
            step_value = int(step_value_str)
        except Exception as e:
            raise TypeError("Step value must be an integer", e)

    # Star ranges
    if range_str[0] == "*":
        r_start_int, r_stop_int = limits
    else:
        # Range ranges
        if "-" in range_str:
            r_start, r_stop = range_str.split("-")
        else:
            # Atomic ranges
            r_start = r_stop = range_str
        try:
            r_start_int = (
                name_substs[r_start] if not r_start.isnumeric() else int(r_start)
            )
            r_stop_int = name_substs[r_stop] if not r_stop.isnumeric() else int(r_stop)
            # Cast should always work as we're checking against isnumeric
        except KeyError as e:
            raise Exception(f"Name subtitution failed for {r_start} or {r_stop}", e)

    # Rectify the order of start and stop.
    if r_start_int > r_stop_int:
        r_start_int, r_stop_int = r_stop_int, r_start_int
    # Check our values are within the specified ranage limits
    if r_start_int < limits[0] or r_stop_int > limits[1]:
        raise Exception(f"Time specified outside given range {limits}")
    return set(range(r_start_int, r_stop_int + 1, step_value))


def generate_times(
    specification: str, range_spec: str, name_substs: dict[str, int] = {}
) -> list[str]:
    """
    Generate a list of numbers based on the given specification.
    The specification may consist of one or more ranges that need to
    each be expanded.
    """
    ranges = specification.split(",")
    range_limit_start, range_limit_stop = [int(i) for i in range_spec.split("-")]
    times = set()
    for r in ranges:
        rg = generage_range(r, (range_limit_start, range_limit_stop), name_substs)
        times |= rg
    # Sorted before being stringified to preserve numeric sort
    return [str(i) for i in sorted(list(times))]


month_substs = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}

# We assume week starts at monday. This is locale specific really.
# Sunday could be either 0 or 7. Let's assume 0
day_substs = {"sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6}


def process_cron_line(line: str) -> None:
    minute, hour, day_of_month, month, day_of_week, command = line.split(maxsplit=5)
    minutes = generate_times(minute, "0-59")
    hours = generate_times(hour, "0-23")
    days_of_month = generate_times(day_of_month, "1-31")
    months = generate_times(month, "1-12", name_substs=month_substs)
    days_of_week = generate_times(day_of_week, "0-7", name_substs=day_substs)
    print(f"minute        {' '.join(minutes)}")
    print(f"hour          {' '.join(hours)}")
    print(f"day of month  {' '.join(days_of_month)}")
    print(f"month         {' '.join(months)}")
    print(f"day of week   {' '.join(days_of_week)}")
    print(f"command       {command}")


if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] == "":
        sys.exit('Usage: cronview "*/15 0 1,15 * 1-5 /usr/bin/find"')
    process_cron_line(sys.argv[1])
