import os
from email.mime.text import MIMEText
from smtplib import SMTP
from typing import List, Dict
from mail.enums.server_type import ServerType
from mail.utils.server import get_smtp_server, server_login
from mail.utils.read_file_content import read_file_content
from jinja2 import Environment


class Email:
    def __init__(
            self,
            mail_to: List[str],
            mail_from: str,
            password: str = None,
            subject=None,
            template_variables=None,
            template_path: str = "mail/templates/test.html"
    ):
        if template_variables is None:
            template_variables = {}
        self.debug = os.getenv("debug") == "true"
        self.mail_to = mail_to
        self.mail_from = mail_from
        self.password = password
        self.subject = subject
        self.server_type = ServerType.LOCALHOST if self.debug else ServerType.GMAIL
        self.server = get_smtp_server(self.server_type)
        self.content = read_file_content(template_path)
        self.template_variables = template_variables

    def __get_email_content(self) -> MIMEText:
        message = MIMEText(Environment().from_string(self.content).render(**self.template_variables), "html")
        message['Subject'] = self.subject
        message['To'] = ", ".join(self.mail_to)
        message['From'] = self.mail_from
        return message

    def __process_email(self) -> (MIMEText, SMTP):
        message = self.__get_email_content()

        server = server_login(server=self.server,
                              server_type=self.server_type,
                              username=self.mail_from,
                              password=self.password)
        return message, server

    def __send_email(
            self,
            server: SMTP,
            message: MIMEText
    ):
        try:
            server.sendmail(self.mail_from, self.mail_to, message.as_string())
            server.quit()
        except Exception as e:
            print(e)

    def send(self):
        message, server = self.__process_email()
        self.__send_email(server, message)
