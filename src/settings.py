from pathlib import Path

class Zeebe:
    ZEEBE_HOSTNAME = "zeebe"
    ZEEBE_PORT = 26500
    ZEEBE_MAX_CONNECTION_RETRIES = -1
    BPMN_DUMP_PATH = Path("/opt/working/src/bpmn_dump")