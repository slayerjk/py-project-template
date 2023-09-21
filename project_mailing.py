"""
Sending emails(smtp): reports or simple sending
"""

from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# SIMPLE SEND MAIL FUNCTION
def send_mail(mail_to, mail_from, smtp_server, smtp_port, mail_data):
    message = MIMEMultipart()
    message["From"] = mail_from
    message["Subject"] = 'TEST MAILING SUBJECT'
    message["To"] = mail_to
    rcpt_to = mail_to
    message.attach(MIMEText(mail_data, "html"))
    with SMTP(smtp_server, smtp_port) as mail:
        data = message.as_string()
        mail.ehlo()
        mail.sendmail(mail_from, rcpt_to, data)
        mail.quit()


# EMAIL REPORT
def send_mail_report(smtp_server, smtp_port, log_name, subj_date, main_log,
                     from_addr, to_addr_list_admins=None, to_addr_list_users=None):
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
            with SMTP(smtp_server, smtp_port) as mail:
                data = message.as_string()
                mail.ehlo()
                mail.sendmail(from_addr, rcpt_to, data)
                mail.quit()
                if type == 'error':
                    print(f'{datetime.now()} - INFO - SUCCEEDED: sending email error report\n')
                else:
                    print(f'{datetime.now()} - INFO - SUCCEEDED: sending email final report\n')
        except Exception as e:
            if type == 'error':
                raise Exception(f'{datetime.now()} - WARNING - FAILED: sending email error report, moving on...\n{e}')
            else:
                raise Exception(f'{datetime.now()} - WARNING - FAILED: sending email final report, moving on...\n{e}')
