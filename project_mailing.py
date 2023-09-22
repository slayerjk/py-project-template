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
    # Try to log in to server and send email
    with SMTP(smtp_server, smtp_port) as server:
        # DEBUG: 1 or 2(with timestamp)
        # server.set_debuglevel(1)

        # USE AUTH: STARTTLS IF LOGIN IS NOT NONE
        if login and password:
            context = create_default_context()
            server.starttls(context=context)  # Secure the connection
            server.login(login, password)
        server.ehlo()  # Can be omitted
        # Send email here
        message = MIMEMultipart()
        message["From"] = mail_from
        message["Subject"] = 'TEST MAILING SUBJECT'
        message["To"] = mail_to
        rcpt_to = mail_to
        message.attach(MIMEText(mail_data, "html"))
        data = message.as_string()
        server.sendmail(mail_from, rcpt_to, data)


# EMAIL REPORT W/WO AUTH
def send_mail_report(smtp_server, smtp_port, log_name, subj_date, main_log,
                     from_addr, to_addr_list_admins=None, to_addr_list_users=None, login=None, password=None):
    """
    To send email report at.
    By default, at the end of the script only.
    Args are:
        - type: may be:
            'error' - send whole log with error
            'report' - send whole log after script done
        - log_name - log file name(to send as report)
        - subj_date - date format to insert into subject
        - main_log - whole log data(if has one), to write status
    """
    message = MIMEMultipart()
    message["From"] = from_addr

    with open(main_log, 'a'):
        if type == 'error':
            print(f'{datetime.now()} - INFO - STARTED: sending email error report')
            message["Subject"] = f'appname - Script Error({subj_date})'
            message["To"] = ', '.join(to_addr_list_admins)
            rcpt_to = to_addr_list_admins
        elif type == 'report':
            print(f'{datetime.now()} - INFO - STARTED: sending email final report')
            message["Subject"] = f'appname - Script Report({subj_date})'
            message["To"] = ', '.join(to_addr_list_users)
            rcpt_to = to_addr_list_users

        with open(log_name, 'r') as log:
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
                server.sendmail(from_addr, rcpt_to, data)
                server.quit()
                if type == 'error':
                    print(f'{datetime.now()} - INFO - SUCCEEDED: sending email error report\n')
                else:
                    print(f'{datetime.now()} - INFO - SUCCEEDED: sending email final report\n')
        except Exception as e:
            if type == 'error':
                raise Exception(f'{datetime.now()} - WARNING - FAILED: sending email error report, moving on...\n{e}')
            else:
                raise Exception(f'{datetime.now()} - WARNING - FAILED: sending email final report, moving on...\n{e}')
