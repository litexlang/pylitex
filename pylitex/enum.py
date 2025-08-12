from enum import Enum

class RunBatchModel(Enum):
    MULTITHREAD = "multithread"
    MULTIPROCESS = "multiprocess"
    AUTO = "auto"