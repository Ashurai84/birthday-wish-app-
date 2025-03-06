import datetime
import csv
import tkinter as tk
from tkinter import messagebox

# 📌 Load Birthdays
def load_birthdays():
    birthdays = []
    try:
        with open("birthdays.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                birthdays.append(row)
    except FileNotFoundError:
        print("❌ Error: birthdays.csv file not found!")
    return birthdays

# 🎉 Check Today's Birthdays
def check_birthdays():
    today = datetime.date.today().strftime("%Y-%m-%d")
    birthdays = load_birthdays()
    today_birthdays = [b for b in birthdays if b["DOB"] == today]

    if today_birthdays:
        for person in today_birthdays:
            show_popup(person["Name"])
            print(f"🎂 Today is {person['Name']}'s Birthday!")
    else:
        print("✅ No birthdays today.")

# 🎈 Show Popup Notification
def show_popup(name):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("🎂 Birthday Reminder!", f"🎉 It's {name}'s Birthday today! 🥳")
    root.destroy()

# 🚀 Run the Birthday Check
if __name__ == "__main__":
    check_birthdays()
