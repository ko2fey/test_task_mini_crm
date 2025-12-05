from enum import Enum

class StatusList(str, Enum):
    IN_QUEUE = "in_queue"
    NEW = "new"
    IN_PROGRESS = "in_progress"
    DONE = "done"