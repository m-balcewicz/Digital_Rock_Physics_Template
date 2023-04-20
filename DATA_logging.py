import datetime
import os
import os.path


def new_log_entry(input_str):
    log_file_name = 'DRP.log'
    log_file_path = 'Q:\CODING_WORLD\PYTHON_WORLD\Digital_Rock_Physics'
    log_file = log_file_path + log_file_name
    format_out = '%Y-%m-%d %H:%M:%S'
    with open(log_file_path, 'a') as f:
        f.write(f"{datetime.datetime.now().strftime(format_out)} {input_str}\n")
    return 'TRUE'
