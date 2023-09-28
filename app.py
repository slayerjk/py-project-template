# IMPORT PROJECTS PARTS
from project_static import (appname, start_date_n_time, logging, logs_dir, logs_to_keep, app_log_name,\
    script_data

from project_helper import count_estimated_time, files_rotate, check_file, check_create_dir

# from app_functions import 

# MAILING IMPORTS
# from project_static import mailing_data, smtp_server, smtp_port, smtp_login, smtp_pass, smtp_from_addr,\
#     mail_list_admins, mail_list_users
# from project_mail_report import send_mail_report, send_mail


# SCRIPT STARTED ALERT
logging.info(f'SCRIPT WORK STARTEDED: {appname}')
logging.info(f'Script Starting Date&Time is: {str(start_date_n_time)}')
logging.info('----------------------------\n')


# CHECKING DATA FILES

# CHECK DATA DIR EXIST/CREATE
check_create_dir(script_data)

# CHECK LOGS DIR EXIST/CREATE
check_create_dir(logs_dir)

# CHECK MAILING DATA
if not check_file(mailing_data):
    logging.warning('NO MAILING DATA PRESENT!')

"""
OTHER CODE GOES HERE
"""


# POST-WORK PROCEDURES

# FINISH JOBS
logging.info('#########################')
logging.info('SUCCEEDED: Script job done!')

logging.info(count_estimated_time(start_date_n_time))
logging.info('----------------------------')
files_rotate(logs_dir, logs_to_keep, app_log_name)
