import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config  

def send_email(to_email, name, wish):
    msg = MIMEMultipart()
    msg["From"] = config.EMAIL_ADDRESS
    msg["To"] = to_email
    msg["Subject"] = f"🎉 Happy Birthday, {name}!"

    message = f"""
    <html>
        <body>
            <h2>🎉 Happy Birthday {name}! 🎂</h2>
            <p>{wish}</p>
            <p>🎁 Enjoy your special day!</p>
        </body>
    </html>
    """

    msg.attach(MIMEText(message, "html"))

    try:
        server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {name} ({to_email})")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
