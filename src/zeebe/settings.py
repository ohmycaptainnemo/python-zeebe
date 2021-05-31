from pathlib import Path
import os

from .utils import error_handler, log_decorator


PORT = int(os.environ.get("API_PORT", "5555"))


class Zeebe:
    ZEEBE_HOSTNAME = "zeebe"
    ZEEBE_PORT = 26500
    ZEEBE_MAX_CONNECTION_RETRIES = -1
    BPMN_DUMP_PATH = Path("/opt/working/src/zeebe/bpmn_dump")
    TASK_DEFAULT_PARAMS = {
        "exception_handler": error_handler,
        "timeout": 60000,
        "before": [log_decorator],
        "after": [log_decorator],
    }
