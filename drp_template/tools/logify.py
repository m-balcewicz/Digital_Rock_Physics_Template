import datetime
import os
import os.path


def mk_log(input_str, print_log=True):
    """
    Write a log entry to a file and optionally print it to the console.

    Parameters:
    - input_str (str): The log entry to be written.
    - print_log (bool, optional): If True, the log entry will be printed to the console. Default is True.

    Returns:
    - bool: True if the log entry was successfully written, False otherwise.
    """
    # log_file_path = '/data/GZB/mbalcewicz/STUDIES/TRM/AUTOMATIONS/heidi_toolkit.log'
    # log_file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/heidi_toolkit/heidi_toolkit.log'
    # log_file_path = '/Users/martin/Library/Mobile Documents/com~apple~CloudDocs/MYDATA/CODING_WORLD/PYTHON_WORLD/heidi_toolkit/heidi_toolkit/A-TRM.log'
    # log_file_path = '/DRP.log'
    log_file_path = '../drp_template/tools/maintenance.log'
    formatOut = '%Y-%m-%d %H:%M:%S'

    try:
        with open(log_file_path, 'a') as file:
            current_time = datetime.datetime.now().strftime(formatOut)
            file.write(f'{current_time} {input_str}\n')

        if print_log:
            print(input_str)

    except Exception as e:
        print(f"Error writing to log file: {e}")
        return False

    return True
