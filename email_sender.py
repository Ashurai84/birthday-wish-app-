import smtplib
from email.mime.text import MIMEText
import random

EMAIL_ADDRESS = "Raia40094@gmail.com"
EMAIL_PASSWORD = " quvi ukfc ihuq vngu"  

# 🎉 Fun Birthday Messages with GIFs
BIRTHDAY_WISHES = [
    ("🎂 Happy Birthday! 🎉 Wishing you a fantastic day!", "https://media.giphy.com/media/xT1XGzXhVfoaHnNPvG/giphy.gif"),
    ("🎊 Have a wonderful year ahead! 🥳", "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExMHVkNGoycGY0dTd1bjg3OTB2aXFsYWJwZ2lmaXViNWFibnh3amh2cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/11sBLVxNs7v6WA/giphy.gif"),
    ("🎁 Hope all your wishes come true! 🎈", "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif")
]

def send_email(to_email, name):
    """Send a personalized birthday wish via email."""
    subject = f"🎂 Happy Birthday and wish veryy  muchhh, {name}!"
    message, gif_url = random.choice(BIRTHDAY_WISHES)

    # HTML email with GIF
    body = f"""
    <html>
    <body>
        <h2>🎉 {message}</h2>
        <img src="{gif_url}" alt="Birthday GIF" width="300">
        <p>Have a fantastic day! 🎈</p>
    </body>
    </html>
    """

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        print(f"✅ Email sent to {name} ({to_email})")
        return True
    except Exception as e:
        print(f"❌ Failed to send email to {name}: {e}")
        return False
