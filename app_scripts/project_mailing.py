"""
Settings and functions for e-mail(smtp) reporting
"""

from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ssl import create_default_context


# SIMPLE SEND EMAIL FUNCTION W/WO AUTH
def send_mail(mail_to, mail_from, smtp_server, smtp_port, mail_data, login=None, password=None):
    with SMTP(smtp_server, smtp_port) as server:
        # DEBUG: 1 or 2(with timestamp)
        # server.set_debuglevel(1)

        # USE AUTH: STARTTLS IF LOGIN IS NOT NONE
        if login and password:
            context = create_default_context()
            server.starttls(context=context)
            server.login(login, password)
        server.ehlo()
        message = MIMEMultipart()
        message["From"] = mail_from
        message["Subject"] = 'TEST MAILING SUBJECT'
        message["To"] = mail_to
        rcpt_to = mail_to
        message.attach(MIMEText(mail_data, "html"))
        data = message.as_string()
        server.sendmail(mail_from, rcpt_to, data)
        return 'Success'


# EMAIL REPORT W/WO AUTH
def send_mail_report(appname, to_mail_list, mail_from, smtp_server, smtp_port, log_file, login=None, password=None,):
    """
    To send email report at.
    By default, at the end of the script only.

    Args:
        appname: may be appname from project_static
        to_mail_list: emails list, maybe mail_list_users/mail_list_admins from project_static
        mail_from: may be smtp_from_addr from project_static
        smtp_server: may be smtp_server from project_static
        smtp_port: may be smtp_port from project_static
        log_file: any file, maybe app_log_name from project_static
        login: may be smtp_login from project_static
        password: may be smtp_pass from project_static
    """
    message = MIMEMultipart()
    message["From"] = mail_from
    message["Subject"] = f'{appname} - Script Report({datetime.now()})'
    message["To"] = ', '.join(to_mail_list)
    rcpt_to = to_mail_list

    with open(log_file, 'r') as log:
        report = log.read()
        message.attach(MIMEText(report, "plain"))
    try:
        with SMTP(smtp_server, smtp_port) as server:
            # DEBUG: 1 or 2(with timestamp)
            # server.set_debuglevel(1)

            # USE AUTH: STARTTLS IF LOGIN IS NOT NONE
            if login and password:
                context = create_default_context()
                server.starttls(context=context)  # Secure the connection
                server.login(login, password)
            data = message.as_string()
            server.ehlo()
            server.sendmail(mail_from, rcpt_to, data)
            server.quit()
    except Exception as e:
        raise Exception(e)
    else:
        return 'Success'
