"""
Settings and functions for e-mail(smtp) sending/reporting
"""

from datetime import datetime
from smtplib import SMTP
from email.message import EmailMessage
from ssl import create_default_context, OPENSSL_VERSION
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText


# SIMPLE SEND EMAIL FUNCTION W/WO AUTH
def send_mail(mail_to, mail_from, smtp_server, smtp_port, mail_data, subject='TEST EMAIL', login=None, password=None):
    """
    Simple email send, using 25(SMTP without auth) or 587(TLS, with auth) ports.
    Use Auth method(starttls()) if login & password are present.
    Sender(mail_to may be list or single sender.

    Args:
        mail_to: list or tuple(for several emails) or str for single address
        mail_from: str, mail from field
        smtp_server: str, server ip/name
        smtp_port: int/str, server's port
        mail_data: str, mail body
        subject: str, mail subject
        login: str, login
        password: str, password
    """
    # message = MIMEMultipart() # if use MIMEMultipart
    message = EmailMessage() # uf use EmailMessage

    message["From"] = mail_from
    message["Subject"] = subject

    if isinstance(mail_to, (list, tuple)):
        message["To"] = ', '.join(mail_to)
    else:
        message["To"] = mail_to

    # message.attach(MIMEText(mail_data, "html")) # if use MIME
    # data = message.as_string() # if use MIME
    message.set_content(mail_data, subtype='html')  # if use EmailMessage

    with SMTP(smtp_server, smtp_port) as server:
        # DEBUG: 1 or 2(with timestamp)
        # print(ssl.OPENSSL_VERSION)
        # server.set_debuglevel(1)
        
        # USE AUTH: STARTTLS IF LOGIN & PASS IS NOT NONE
        if login and password:
            context = create_default_context()
            server.starttls(context=context)
            server.login(login, password)

        # server.sendmail(mail_from, mail_to, data) # if use MIME
        server.send_message(message, mail_from, mail_to) # if use EmailMessage

        server.quit()


# EMAIL REPORT W/WO AUTH
def send_mail_report(appname, mail_to, mail_from, smtp_server, smtp_port, log_file, login=None, password=None,):
    """
    To send email report at.
    By default, at the end of the script only.
    Use Auth method(starttls()) if login & password are present.
    Sender(mail_to may be list or single sender.

    Args:
        appname: str, your app name
        mail_to: list or tuple(for several emails) or str for single address
        mail_from: str, mail from field
        smtp_server: str, server ip/name
        smtp_port: int/str, server's port
        log_file: any text file
        login: str, login
        password: str, password
    """
    message = MIMEMultipart()
    message["From"] = mail_from
    message["Subject"] = f'{appname} - Script Report({datetime.now()})'

    if isinstance(mail_to, (list, tuple)):
        message["To"] = ', '.join(mail_to)
    else:
        message["To"] = mail_to

    data = message.as_string()

    with open(log_file, 'r') as log:
        report = log.read()
        message.attach(MIMEText(report, "plain"))
        with SMTP(smtp_server, smtp_port) as server:
            # DEBUG: 1 or 2(with timestamp)
            # server.set_debuglevel(1)
            # print(ssl.OPENSSL_VERSION)

            # USE AUTH: STARTTLS IF LOGIN IS NOT NONE
            if login and password:
                context = create_default_context()
                server.starttls(context=context)  # Secure the connection
                server.login(login, password)

            server.sendmail(mail_from, mail_to, data)
            server.quit()
