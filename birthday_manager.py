import csv

BIRTHDAY_FILE = "birthday_data.csv"

def add_birthday(name, email, date):
    """Adds a birthday entry to the CSV file."""
    with open(BIRTHDAY_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, email, date])

def load_birthdays():
    """Loads all birthdays from CSV file."""
    try:
        with open(BIRTHDAY_FILE, "r") as file:
            return [line.strip().split(",") for line in file.readlines()]
    except FileNotFoundError:
        open(BIRTHDAY_FILE, "w").close()
        return []

def search_birthday(query):
    """Searches for a birthday by name."""
    return [b for b in load_birthdays() if query.lower() in b[0].lower()]
