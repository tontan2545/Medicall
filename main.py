import os
from mail.mail import Email
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    email = Email(
        mail_to=["tontan2545@gmail.com"],
        mail_from="medicallnoreply@gmail.com",
        password=os.getenv("GMAIL_PASSWORD"),
        subject="Test",
    )
    email.send()
