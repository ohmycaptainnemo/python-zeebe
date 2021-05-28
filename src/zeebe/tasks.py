import logging
from typing import Dict, List, Optional
from pyzeebe import ZeebeWorker

# from .utils import TaskDefaults
from .settings import Zeebe

logger = logging.getLogger()

worker = ZeebeWorker(
    hostname=Zeebe.ZEEBE_HOSTNAME,
    port=Zeebe.ZEEBE_PORT,
    max_connection_retries=Zeebe.ZEEBE_MAX_CONNECTION_RETRIES,
)


@worker.task(task_type="package-items")
def package_items(collectedItems: int, data: str, aggregateList: List) -> Optional[Dict]:
    collectedItems += 1
    aggregateList.append(data)

    return {"collectedItems": collectedItems, "aggregateList": aggregateList}


@worker.task(task_type="process-item")
def package_item(data: str, aggregateList: List) -> Optional[Dict]:
    aggregateList.append(data)

    return {"aggregateList": aggregateList}
