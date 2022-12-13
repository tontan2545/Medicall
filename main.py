import os
from mail.mail import Email
from server.server import Server
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    email = Email(
        mail_to=["tasha.tanarugs@gmail.com"],
        mail_from="medicallnoreply@gmail.com",
        password=os.getenv("GMAIL_PASSWORD"),
        subject="Test",
        template_path="mail/templates/report.html"
    )
    email.send()

    # server = Server()
    # server.start()
