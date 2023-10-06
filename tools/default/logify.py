import datetime
import os
import os.path


def mk_log(input_str):
    # log_file_path = '/data/GZB/mbalcewicz/STUDIES/TRM/AUTOMATIONS/heidi_toolkit.log'
    # log_file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/heidi_toolkit/heidi_toolkit.log'
    log_file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/heidi_toolkit/heidi_toolkit/A-TRM.log'
    formatOut = '%Y-%m-%d %H:%M:%S'

    with open(log_file_path, 'a') as file:
        current_time = datetime.datetime.now().strftime(formatOut)
        file.write(f'{current_time} {input_str}\n')

    new_log_entry = 'TRUE'
    return new_log_entry
