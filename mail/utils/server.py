from smtplib import SMTP
from mail.enums.server_type import ServerType


def get_smtp_server(variant: ServerType) -> SMTP:
    if variant == ServerType.LOCALHOST:
        return SMTP('localhost', 1025)
    if variant == ServerType.GMAIL:
        return SMTP('smtp.gmail.com', 587)
    raise Exception("Unknown server type")


def server_login(server: SMTP, server_type: ServerType, username: str, password: str) -> SMTP:
    if server_type == ServerType.LOCALHOST:
        return server
    if password is None:
        raise Exception("Password not provided!")
    server.starttls()
    server.login(username, password)
    return server
