#!/usr/bin/env python3

# IMPORT PROJECTS PARTS
from project_helper import count_estimated_time, files_rotate
from project_common import appname, start_date_n_time, logging, logs_dir, logs_to_keep, app_log_name
from project_mail_report import send_mail_option, send_mail_report

# PROJECT DATA
"""
Section for project's vars
"""

# MAIN FUNCTIONS
"""
Section for your app's various functions
"""

# MAIN WORKFLOW

# SCRIPT STARTED ALERT
logging.info(f'SCRIPT WORK STARTEDED: {appname}')
logging.info(f'Script Starting Date&Time is: {str(start_date_n_time)}')
logging.info('----------------------------\n')

# RUN FUNCTIONS

# POST-WORK PROCEDURES

# FINISH JOBS
logging.info('#########################')
logging.info('SUCCEEDED: Script job done!')

logging.info(count_estimated_time(start_date_n_time))
logging.info('----------------------------')
files_rotate(logs_dir, logs_to_keep, app_log_name)
if send_mail_option == 'yes':
    send_mail_report('report', app_log_name, start_date_n_time, app_log_name)
