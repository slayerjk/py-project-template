"""
Various Helper functions:
 - files_rotate
 - functions decorator
 - count estimated time
 - check dir exist
 - check file exist
 """

from pathlib import Path
from os import remove, mkdir, path
from app_scripts.project_static import logging


# FUNCTION CALL DECORATOR
def func_decor(action='PRINTING FUNC DESCR', level='warn'):
    """

    Args:
        action: str, decored function description, "logging started" or "loggiing started for" {obj=user_name}
        level: default: warn, crit; func fail: warn->skip error, crit->exit program

    Returns: decored func

    """
    def inner(func):
        def wrapper(*args, **kwargs):
            logging.info(f'STARTED: {action}')
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                if level == 'crit':
                    logging.error(f'FAILED: {action}, exiting\n{e}')
                    exit()
                else:
                    logging.warning(f'FAILED: {action}, skipping\n{e}')
            else:
                logging.info(f'DONE: {action}\n')
                return result
        return wrapper
    return inner


# FILES ROTATION (LOGS/OTHER)
@func_decor('file/logs rotation')
def files_rotate(path_to_rotate, num_of_files_to_keep):
    """
    This function is for log rotation.
    ARGS:
        path_to_rotate: absolute PATH of logs location
        num_of_files_to_keep: number of LOGS to keep
            delete rest
    """
    count_files_to_keep = 1
    basepath = sorted(Path(path_to_rotate).iterdir(), key=path.getctime, reverse=True)
    for entry in basepath:
        if count_files_to_keep > num_of_files_to_keep:
            remove(entry)
        count_files_to_keep += 1


# CHECK FILE EXIST
def check_file(file_path):
    return path.isfile(file_path)


# CHECK DIR EXIST
def check_create_dir(dir_path):
    if not path.isdir(dir_path):
        mkdir(dir_path)
