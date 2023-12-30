import logging
from datetime import datetime
import time


def format_address(address_str):
    """ Format or clean the address string. """
    return address_str.strip()

def log_error(error_msg):
    """ Log an error message with the current timestamp. """
    logging.error(f"{datetime.now()} - ERROR - {error_msg}")

def notify_user_to_solve_captcha():
    """ Prompt the user to solve a CAPTCHA. """
    input("Please solve the CAPTCHA and then press Enter to continue...")
    time.sleep(5)

def convert_list_to_string(list_items, separator=', '):
    """ Convert a list of items to a string with a specified separator. """
    return separator.join(list_items)

def log_info(message):
    """ Log an informational message with the current timestamp. """
    logging.info(f"{datetime.now()} - INFO - {message}")