from plyer import notification

def send_notification(name):
    notification.notify(
        title="🎂 Birthday Reminder!",
        message=f"Today is {name}'s birthday! Don't forget to wish!",
        timeout=10
    )
# Compare this snippet from email_sender.py: