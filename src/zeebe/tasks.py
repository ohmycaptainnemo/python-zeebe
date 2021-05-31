import logging
from typing import Dict, List, Optional
from pyzeebe import ZeebeWorker

from .settings import Zeebe

logger = logging.getLogger()

worker = ZeebeWorker(
    hostname=Zeebe.ZEEBE_HOSTNAME,
    port=Zeebe.ZEEBE_PORT,
    max_connection_retries=Zeebe.ZEEBE_MAX_CONNECTION_RETRIES,
)


@worker.task(task_type="package-items", **Zeebe.TASK_DEFAULT_PARAMS)
def package_items(collectedItems: int, data: str, aggregateList: List) -> Optional[Dict]:
    """Package items task definition.

    Args:
        collectedItems (int): Number of collected items.
        data (str): Data payload.
        aggregateList (List): List containing aggregated data.

    Returns:
        Optional[Dict]: Dictionary containing variables that are returned by this task.
    """
    collectedItems += 1
    aggregateList.append(data)

    return {"collectedItems": collectedItems, "aggregateList": aggregateList}


@worker.task(task_type="package-item", **Zeebe.TASK_DEFAULT_PARAMS)
def package_item(
    errorHandlerTest: bool, failureHandlerTest: bool, data: str, aggregateList: List
) -> Optional[Dict]:
    """Package item task definition.

    Args:
        errorHandlerTest (bool): One can set this flag (i.e. throught the API) to simulate/cause an "error" in this task.
        In this case the error is a MemoryError.

        failureHandlerTest (bool): One can set this flag (i.e. through the API) to simulate/cause a "failure" in this task.
        In this case the error is a ConnectionError.

        data (str): The data payload.
        aggregateList (List): The aggregated list of payload.

    Raises:
        ConnectionError: ConnectionError artificially/intentionally raised in this case to simulate a situation where a
        ConnectionError happens, like disconnection for an API or server.

        MemoryError: MemoryError artificially/intentionally raised to indicate a fatal/unrecoverable error like memory error/leak.

    Returns:
        Optional[Dict]: The aggregated payload.
    """
    aggregateList.append(data)
    if failureHandlerTest:
        raise ConnectionError
    if errorHandlerTest:
        raise MemoryError
    return {"aggregateList": aggregateList}
