"""
This package must contain all tasks to be executed by celery.
"""
from celery.exceptions import Ignore


class TaskFailure(Ignore):
    """
    Class that represents the failure of a task.
    """

    def __init__(self, reason):
        super(TaskFailure, self).__init__(reason)
