"""
This module contains the current time variables.
"""

from datetime import datetime


def current_time_stamp():
    """
    Returns the current time stamp as an integer.
    """
    time_stamp = datetime.now().timestamp()
    time_stamp = int(time_stamp)
    return time_stamp
