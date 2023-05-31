"""
Settings and functions for e-mail(smtp) reporting
"""
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# SMTP DATA(WITHOUT AUTH); NO BY DEFAULT
send_mail_option = 'no'
smtp_server = '<YOUR-SMTP-SERVER>'
from_addr = 'YOUR-APP-NAME@EX.COM'
to_addr_list_users = ['USER@EX.COM']
to_addr_list_admins = ['ADMIN@EX.COM']
smtp_port = 25

# EMAIL REPORT ###
"""
To send email report at.
By default, at the end of the script only.
Args are:
    - report_type: may be:
        'error' - send whole log with error
        'report' - send whole log after script done
    - log_name - log file name(to send as report)
    - subj_date - date format to insert into subject
    - main_log - whole log data(if has one), to write status
"""


def send_mail_report(report_type, log_name, subj_date, main_log):
    message = MIMEMultipart()
    message["From"] = from_addr

    with open(main_log, 'a'):
        if send_mail_option == 'yes':
            if report_type == 'error':
                print(f'{datetime.now()} - INFO - STARTED: sending email error report')
                message["Subject"] = f'appname - Script Error({subj_date})'
                message["To"] = ', '.join(to_addr_list_admins)
                rcpt_to = to_addr_list_admins
            elif report_type == 'report':
                print(f'{datetime.now()} - INFO - STARTED: sending email final report')
                message["Subject"] = f'appname - Script Report({subj_date})'
                message["To"] = ', '.join(to_addr_list_users)
                rcpt_to = to_addr_list_users
            
            with open(log_name, 'r') as log:
                report = log.read()
                message.attach(MIMEText(report, "plain"))
            try:
                with SMTP(smtp_server, smtp_port) as send_mail:
                    data = message.as_string()
                    send_mail.ehlo()
                    send_mail.sendmail(from_addr, rcpt_to, data)
                    send_mail.quit()
                    if report_type == 'error':
                        print(f'{datetime.now()} - INFO - SUCCEEDED: sending email error report\n')
                    else:
                        print(f'{datetime.now()} - INFO - SUCCEEDED: sending email final report\n')
            except Exception as e:
                if report_type == 'error':
                    raise Exception(f'{datetime.now()} - FAILED: sending email error report, moving on...\n{e}')
                else:
                    raise Exception(f'{datetime.now()} - FAILED: sending email final report, moving on...\n{e}')
