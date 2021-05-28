from pathlib import Path
import os

PORT = int(os.environ.get("API_PORT", "5555"))


class Zeebe:
    ZEEBE_HOSTNAME = "zeebe"
    ZEEBE_PORT = 26500
    ZEEBE_MAX_CONNECTION_RETRIES = -1
    BPMN_DUMP_PATH = Path("/opt/working/src/zeebe/bpmn_dump")
