import tkinter as tk
from tkinter import messagebox
import datetime
import csv
import random
import email_sender  

# 🎊 Random Birthday Wishes
wishes = [
    "Happy Birthday! 🎂 Wishing you all the happiness!",
    "Many many happy returns of the day! 🎉",
    "Hope your special day brings you joy & love! 🎁",
    "Cheers to another year of amazing adventures! 🥳"
]

# Load Birthdays from CSV
def load_birthdays():
    birthdays = []
    try:
        with open("birthdays.csv", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                birthdays.append(row)
    except FileNotFoundError:
        messagebox.showerror("Error", "birthdays.csv file not found!")
    return birthdays

# 🎯 Countdown Timer
def update_timer():
    today = datetime.date.today()
    birthdays = load_birthdays()
    if not birthdays:
        countdown_label.config(text="No birthdays saved!")
        return

    upcoming = min(birthdays, key=lambda b: datetime.datetime.strptime(b["DOB"], "%Y-%m-%d").date())
    bday = datetime.datetime.strptime(upcoming["DOB"], "%Y-%m-%d").date()
    delta = (bday - today).days
    countdown_label.config(text=f"🎂 {upcoming['Name']}'s Birthday in {delta} days!")

# ✉ Send Birthday Email
def send_birthday_wish():
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showerror("Error", "Select a person from the list!")
        return

    birthdays = load_birthdays()
    selected_birthday = birthdays[selected_index[0]]
    email_sender.send_email(selected_birthday["Email"], selected_birthday["Name"], random.choice(wishes))

# 🌙 Dark Mode Toggle
def toggle_dark_mode():
    if root.cget("bg") == "#fce4ec":
        root.configure(bg="#212121")
        label_title.config(bg="#212121", fg="white")
        countdown_label.config(bg="#212121", fg="white")
        listbox.config(bg="#424242", fg="white")
    else:
        root.configure(bg="#fce4ec")
        label_title.config(bg="#fce4ec", fg="black")
        countdown_label.config(bg="#fce4ec", fg="black")
        listbox.config(bg="white", fg="black")

# 🎈 Tkinter UI
root = tk.Tk()
root.title("🎂 Birthday Wishes App")
root.geometry("500x400")
root.configure(bg="#fce4ec")

label_title = tk.Label(root, text="🎂 Birthday Wishes App", font=("Arial", 14, "bold"), bg="#fce4ec", fg="black")
label_title.pack(pady=10)

countdown_label = tk.Label(root, text="", font=("Arial", 12), bg="#fce4ec")
countdown_label.pack()

listbox = tk.Listbox(root, height=5, font=("Arial", 12))
for b in load_birthdays():
    listbox.insert(tk.END, f"{b['Name']} - {b['DOB']}")
listbox.pack(pady=10)

send_button = tk.Button(root, text="🎉 Send Wish", font=("Arial", 12), command=send_birthday_wish)
send_button.pack(pady=5)

dark_mode_btn = tk.Button(root, text="🌙 Dark Mode", font=("Arial", 12), command=toggle_dark_mode)
dark_mode_btn.pack()

# 🔄 Update Timer on Start
update_timer()

root.mainloop()
