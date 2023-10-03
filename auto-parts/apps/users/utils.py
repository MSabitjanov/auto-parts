def default_working_hours():
    week_days = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    working_hours = [
        {
            "day": day,
            "is_open": False,
            "hours": [{"start": "00:00", "end": "00:00"}],
        }
        for day in week_days
    ]
    return working_hours
