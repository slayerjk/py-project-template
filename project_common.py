'''
Common settings and functions for project
'''

import logging
from datetime import datetime
from os import mkdir, path

###################
### COMMON DATA ###

### SCRIPT APPNAME(FOR SEND MAIL FUNCTION, LOGNAME, ETC)
appname = 'YOUR-PROJECT-NAME'

### SCRIPT DATA DIR
'''
By default script uses script's location dir.
If you need custom path for script(sensitive) data, 
set custom_script_data_path = 'yes'
'''
custom_script_data_path = 'no'
if custom_script_data_path == 'yes':
    script_data = '<YOUR ABS PATH>'
else:
    script_data = 'script_data'

### SET TIME TO
start_date_n_time = datetime.now()
start_date = start_date_n_time.strftime('%d-%m-%Y')

#######################
### LOGGING SECTION ###

### LOGS LOCATION
'''
By default script uses script's location dir.
If you need custom path for logs, 
set custom_logs_path = 'yes'
'''
custom_logs_path_option = 'no'
'''
custom logs path example(with your appname in it): 
custom_logs_path =  f'/var/logs/{appname}'
'''
custom_logs_path = '<YOUR ABS PATH FOR SCRIPTS LOGS>'

if custom_logs_path_option == 'yes':
    logs_dir = custom_logs_path
else:
    logs_dir = 'logs'

### LOGS FORMAT
'''
logging_format: is for string of log representation
logging_datefmt: is for representation of %(asctime) param
'''
logging_format='%(asctime)s - %(levelname)s - %(message)s'
logging_datefmt = '%d-%b-%Y %H:%M:%S'

### LOG FILEMODE
'''
a - for "append" to the end of file
w - create new/rewrite exist
'''
log_filemode = 'w'

### LOGS TO KEEP AFTER ROTATION
logs_to_keep = 30

### DEFINE LOG NAME
app_log_name = f'{logs_dir}/{appname}_{str(start_date)}.log'

### DEFINE LOGGING SETTINGS
logging.basicConfig(filename=app_log_name, filemode=log_filemode, level=logging.INFO,
                    format=logging_format, datefmt=logging_datefmt)

### CHECK DATA DIR EXIST/CREATE
if not path.isdir(script_data):
    mkdir(script_data)

### CHECK LOGS DIR EXIST/CREATE
if not path.isdir(logs_dir):
    mkdir(logs_dir)

