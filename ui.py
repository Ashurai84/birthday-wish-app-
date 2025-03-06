import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
import json
import main  # Importing main.py to handle functionality
from plyer import notification

# Load saved settings
def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"theme": "Light"}

# Save settings
def save_settings():
    with open("settings.json", "w") as f:
        json.dump(settings, f)

# Toggle Theme
def toggle_theme():
    selected_theme = theme_var.get()
    settings["theme"] = selected_theme
    save_settings()
    apply_theme()

def apply_theme():
    theme = settings.get("theme", "Light")
    bg_color = "#2C2F33" if theme == "Dark" else "#F0F0F0"
    fg_color = "white" if theme == "Dark" else "black"
    btn_bg = "#7289DA" if theme == "Dark" else "#3B82F6"
    
    root.configure(bg=bg_color)
    
    for widget in root.winfo_children():
        if isinstance(widget, (tk.Label, tk.Entry, DateEntry, ttk.Combobox, tk.Listbox)):
            widget.configure(bg=bg_color, fg=fg_color)
        elif isinstance(widget, tk.Button):
            widget.configure(bg=btn_bg, fg="white", font=("Arial", 10, "bold"), bd=0, relief=tk.RAISED)

# Add Birthday
def add_birthday():
    name = name_entry.get()
    email = email_entry.get()
    date = date_entry.get()
    
    if name and email and date:
        with open("birthday_data.csv", "a") as file:
            file.write(f"{name},{email},{date}\n")
        messagebox.showinfo("Success", "Birthday added successfully!")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        date_entry.set_date("")
        load_birthdays()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields!")

# Load Birthdays
def load_birthdays():
    listbox.delete(0, tk.END)
    try:
        with open("birthday_data.csv", "r") as file:
            for line in file:
                name, email, date = line.strip().split(",")
                listbox.insert(tk.END, f"{name} - {date}")
    except FileNotFoundError:
        open("birthday_data.csv", "w").close()

# Search Function
def search_birthday():
    query = search_entry.get().lower()
    listbox.delete(0, tk.END)
    try:
        with open("birthday_data.csv", "r") as file:
            for line in file:
                name, email, date = line.strip().split(",")
                if query in name.lower():
                    listbox.insert(tk.END, f"{name} - {date}")
    except FileNotFoundError:
        pass

# Send Birthday Wishes
def send_birthday_wishes():
    main.send_wishes()
    messagebox.showinfo("Success", "Birthday wishes sent!")

# Desktop Notification
def check_today_birthdays():
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        with open("birthday_data.csv", "r") as file:
            for line in file:
                name, email, date = line.strip().split(",")
                if date == today:
                    notification.notify(
                        title="🎂 Birthday Reminder!",
                        message=f"Today is {name}'s birthday! Don't forget to wish!",
                        timeout=10
                    )
    except FileNotFoundError:
        pass

# UI Setup
root = tk.Tk()
root.title("🎂 Birthday Reminder")
root.geometry("450x550")

settings = load_settings()
theme_var = tk.StringVar(value=settings.get("theme", "Light"))

# Apply Theme
apply_theme()

# UI Elements with Better Styling
tk.Label(root, text="Name:", font=("Arial", 11, "bold")).pack(pady=(10, 2))
name_entry = tk.Entry(root, font=("Arial", 11))
name_entry.pack()

tk.Label(root, text="Email:", font=("Arial", 11, "bold")).pack(pady=(10, 2))
email_entry = tk.Entry(root, font=("Arial", 11))
email_entry.pack()

tk.Label(root, text="Date (YYYY-MM-DD):", font=("Arial", 11, "bold")).pack(pady=(10, 2))
date_entry = DateEntry(root, date_pattern='yyyy-mm-dd', font=("Arial", 11))
date_entry.pack()

tk.Button(root, text="➕ Add Birthday", command=add_birthday, height=1, width=15).pack(pady=5)

# Search
search_entry = tk.Entry(root, font=("Arial", 11))
search_entry.pack(pady=5)
tk.Button(root, text="🔍 Search", command=search_birthday, height=1, width=15).pack()

# Birthday List
listbox = tk.Listbox(root, height=8, font=("Arial", 11))
listbox.pack(pady=5, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox.config(yscrollcommand=scrollbar.set)

# Send Wishes Button
tk.Button(root, text="🎉 Send Wishes", command=send_birthday_wishes, height=1, width=15).pack(pady=5)

# Theme Selection
tk.Label(root, text="Theme:", font=("Arial", 11, "bold")).pack()
theme_menu = ttk.Combobox(root, textvariable=theme_var, values=["Light", "Dark"], state="readonly", font=("Arial", 11))
theme_menu.pack()
tk.Button(root, text="🌙 Apply Theme", command=toggle_theme, height=1, width=15).pack(pady=5)

# Load Birthdays on Start
load_birthdays()
check_today_birthdays()

root.mainloop()
