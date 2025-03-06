import csv
import datetime

BIRTHDAY_FILE = "birthdays.csv"

def get_birthdays():
    """Fetch all birthdays from CSV."""
    birthdays = []
    try:
        with open(BIRTHDAY_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                birthdays.append(row)
    except FileNotFoundError:
        print("⚠️ No birthdays found. Creating an empty file.")
        open(BIRTHDAY_FILE, "w").close()
    return birthdays

def get_todays_birthdays():
    """Get a list of people whose birthday is today."""
    today = datetime.date.today().strftime("%Y-%m-%d")
    return [b for b in get_birthdays() if b["DOB"] == today]

def get_upcoming_birthdays():
    """Get birthdays happening within the next 7 days."""
    today = datetime.date.today()
    upcoming = []
    for b in get_birthdays():
        dob = datetime.datetime.strptime(b["DOB"], "%Y-%m-%d").date()
        days_left = (dob - today).days
        if 0 < days_left <= 7:
            upcoming.append((b["Name"], b["DOB"], days_left))
    return sorted(upcoming, key=lambda x: x[2])  # Sort by days left
