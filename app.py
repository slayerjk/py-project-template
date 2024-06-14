# IMPORT PROJECTS PARTS
from time import perf_counter

from project_static import (
    appname,
    start_date_n_time,
    logging,
    logs_dir,
    logs_to_keep,
    data_files
)

from app_scripts.project_helper import (
    files_rotate,
    check_create_dir,
    func_decor
)

# from app_scripts.app_functions import dummy

# MAILING IMPORTS(IF YOU NEED)
# from project_static import mailing_data, smtp_server, smtp_port, smtp_login, smtp_pass, smtp_from_addr,\
#     mail_list_admins, mail_list_users
# from app_scripts.project_mailing import send_mail_report, send_mail


# SCRIPT STARTED ALERT
logging.info(f'{appname}: SCRIPT WORK STARTED')
logging.info(f'Script Starting Date&Time is: {str(start_date_n_time)}')
logging.info('----------------------------\n')

# START PERF COUNTER
start_time_counter = perf_counter()

# CHECKING DATA DIRS & FILES

# CHECK DATA DIR EXIST/CREATE
func_decor(f'checking {data_files} dir exists and create if not')(check_create_dir)(data_files)

# CHECK MAILING DATA EXIST(IF YOU NEED MAILING)
# func_decor(f'checking {mailing_data} exists', 'crit')(check_file)(mailing_data)

"""
OTHER CODE GOES HERE
"""

# POST-WORK PROCEDURES

# FINISH JOBS
logging.info('#########################')
logging.info('SUCCEEDED: Script job done!')
logging.info(f'Estimated time is: {perf_counter() - start_time_counter}')
logging.info('----------------------------\n')
files_rotate(logs_dir, logs_to_keep)


# MAIL REPORT(IF YOU NEED)
# send_mail_report(appname, mail_list_admins, smtp_from_addr, smtp_server, smtp_port, app_log_name, login=None,
