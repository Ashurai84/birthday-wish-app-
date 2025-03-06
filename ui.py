import tkinter as tk
from tkinter import messagebox
import birthday_manager
import email_sender
import pygame  # For background music
import random  # For confetti effect

# 🎶 Initialize pygame mixer for background music
pygame.mixer.init()
pygame.mixer.music.load("assets/birthday_song.mp3")  # Ensure this file exists
pygame.mixer.music.play(-1)  # Loop indefinitely

# 🎈 Tkinter UI Setup
root = tk.Tk()
root.title("🎂 Birthday Reminder")
root.geometry("500x600")
root.configure(bg="#ffecb3")  # Light yellow background

# 🎊 Confetti Animation
confetti_canvas = tk.Canvas(root, width=500, height=100, bg="#ffecb3", highlightthickness=0)
confetti_canvas.pack()

confetti_particles = []
for _ in range(20):  # Generate confetti
    x = random.randint(0, 500)
    y = random.randint(0, 100)
    size = random.randint(5, 15)
    color = random.choice(["red", "blue", "green", "purple", "orange"])
    particle = confetti_canvas.create_oval(x, y, x+size, y+size, fill=color)
    confetti_particles.append((particle, random.randint(1, 4)))  # Speed

def animate_confetti():
    for particle, speed in confetti_particles:
        confetti_canvas.move(particle, 0, speed)
        x1, y1, x2, y2 = confetti_canvas.coords(particle)
        if y2 > 100:
            confetti_canvas.move(particle, 0, -100)
    root.after(50, animate_confetti)

animate_confetti()

# 📅 List Today's & Upcoming Birthdays
def update_birthday_lists():
    """Update UI with today's and upcoming birthdays."""
    today_birthdays = birthday_manager.get_todays_birthdays()
    upcoming_birthdays = birthday_manager.get_upcoming_birthdays()

    # Clear previous content
    today_listbox.delete(0, tk.END)
    upcoming_listbox.delete(0, tk.END)

    # Add today's birthdays
    if today_birthdays:
        for b in today_birthdays:
            today_listbox.insert(tk.END, f"🎉 {b['Name']} ({b['Email']})")
    else:
        today_listbox.insert(tk.END, "No Birthdays Today 🎂")

    # Add upcoming birthdays
    if upcoming_birthdays:
        for name, dob, days in upcoming_birthdays:
            upcoming_listbox.insert(tk.END, f"📅 {name} - {dob} (in {days} days)")
    else:
        upcoming_listbox.insert(tk.END, "No Upcoming Birthdays 🎈")

# 📩 Send Birthday Wishes
def send_wishes():
    """Send birthday emails to today's birthdays."""
    today_birthdays = birthday_manager.get_todays_birthdays()
    if not today_birthdays:
        messagebox.showinfo("No Birthdays", "🎂 No birthdays today to send wishes.")
        return
    
    success_count = 0
    failed_count = 0
    failed_list = []

    for person in today_birthdays:
        name, email = person["Name"], person["Email"]
        success = email_sender.send_email(email, name)
        if success:
            success_count += 1
        else:
            failed_count += 1
            failed_list.append(name)

    # Show result
    messagebox.showinfo("Email Status", f"✅ Sent: {success_count}\n❌ Failed: {failed_count}")
    if failed_count > 0:
        messagebox.showerror("Failed Emails", f"❌ Could not send to: {', '.join(failed_list)}")

# 📅 UI Elements
tk.Label(root, text="🎂 Today's Birthdays:", font=("Arial", 14, "bold"), bg="#ffecb3", fg="black").pack()
today_listbox = tk.Listbox(root, height=5, font=("Arial", 12), bg="black", fg="white")
today_listbox.pack(pady=5)

tk.Label(root, text="📅 Upcoming Birthdays:", font=("Arial", 14, "bold"), bg="#ffecb3", fg="black").pack()
upcoming_listbox = tk.Listbox(root, height=5, font=("Arial", 12), bg="black", fg="white")
upcoming_listbox.pack(pady=5)

# 📩 Custom Send Wishes Button with Improved Visibility
def on_enter(e):
    send_button.config(bg="#ff5733", fg="white")  # Change color on hover

def on_leave(e):
    send_button.config(bg="red", fg="white")  # Revert to original

send_button = tk.Button(
    root, 
    text="📩 Send Wishes", 
    font=("Arial", 14, "bold"), 
    command=send_wishes, 
    bg="red", 
    fg="white", 
    activebackground="#ff5733",  
    activeforeground="white",
    relief="raised", 
    borderwidth=4, 
    padx=10, 
    pady=5
)

send_button.pack(pady=15)

# 🖱️ Add Hover Effects
send_button.bind("<Enter>", on_enter)
send_button.bind("<Leave>", on_leave)

# 🎈 Load Birthdays on Start
update_birthday_lists()

# 🎂 Run Tkinter Window
root.mainloop()
