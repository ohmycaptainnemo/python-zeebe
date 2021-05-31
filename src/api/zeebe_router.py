from fastapi import APIRouter, File, UploadFile
import logging
from pyzeebe import ZeebeClient
from typing import Dict

from ..zeebe.modules import deploy_workflow_module, run_instance_module, publish_message_module
from ..zeebe.tasks import worker
from ..zeebe.settings import Zeebe


logger = logging.getLogger()

router = APIRouter()


logger.info("Starting client")
client = ZeebeClient(
    hostname=Zeebe.ZEEBE_HOSTNAME,
    port=Zeebe.ZEEBE_PORT,
    max_connection_retries=Zeebe.ZEEBE_MAX_CONNECTION_RETRIES,
)

logger.info("Starting worker")
worker.work(True)


@router.post("/deploy", description="Deploy .bpmn workflow")
async def deploy_workflow(bpmn_file: UploadFile = File(...)):
    """Endpoint for deploying workflows.
    Args:
        bpmn_file (UploadFile, optional): The uploaded .bpmn file. Defaults to File(...).
    """
    return deploy_workflow_module(client, bpmn_file)


@router.post("/run", description="Run an instance of workflow")
async def run_instance(
    bpmn_process_id: str,
    variables: Dict = {
        "collectedItems": 0,
        "numberOfItems": 3,
        "data": {"payload": "123", "orderId": "1"},
        "aggregateList": [],
        "messageTimeout": "PT10S",
        "failureHandlerTest": False,
        "errorHandlerTest": False,
    },
):
    """Endpoint for running new instances.

    Args:
        bpmn_process_id (str): .bpmn process id.

        variables (Dict, optional): The default payload. 
        Defaults to { "collectedItems": 0, 
        "numberOfItems": 3, 
        "data": {"payload": "123", "orderId": "1"}, 
        "aggregateList": [], 
        "messageTimeout": "PT10S",
        "failureHandlerTest": False, 
        "errorHandlerTest": False
        }.
    """
    return run_instance_module(client, bpmn_process_id, variables)


@router.post("/publish", description="Publish message")
async def publish_message(messag_name: str, correlation_key: str, variables: Dict = {}):
    """Endpoint for publishing messages.

    Args:
        messag_name (str): The name of the message.
        correlation_key (str): The correlation key.
        variables (Dict, optional): The payload of the message. Defaults to {}.
    """
    return publish_message_module(client, correlation_key, variables)
