import json
import logging
import os
from typing import Dict

from fastapi import UploadFile
from pyzeebe import ZeebeClient

from ..zeebe.settings import Zeebe

logger = logging.getLogger()


def deploy_workflow_module(client: ZeebeClient, bpmn_file: UploadFile) -> str:
    """Function for deploying workflow from .bpmn file.

    Args:
        client (ZeebeClient): Zeebe client.
        bpmn_file (UploadFile): The uploaded .bpmn file.

    Returns:
        str: Success or error message.
    """
    bpmn_file_path = os.path.join(Zeebe.BPMN_DUMP_PATH, bpmn_file.filename)
    try:
        logger.info("Started saving .bpmn file.")
        with open(bpmn_file_path, "wb+") as file_obj:
            file_obj.write(bpmn_file.file.read())
        logger.info(f"Finished saving .bpmn file. File is at {bpmn_file_path}")
    except IOError:
        logger.error("Could not open or write to the .bpmn file!")

    try:
        client.deploy_workflow(bpmn_file_path)
        success_msg = ".bpmn deployment was successful!"
        logger.info(success_msg)
        return success_msg
    except Exception as e:
        error_response_dict = {
            "code": str(e.__context__.code()),
            "details": e.__context__.details(),
            "debug_string": json.loads(e.__context__.debug_error_string()),
        }
        logger.error(error_response_dict)
        return error_response_dict


def run_instance_module(client: ZeebeClient, bpmn_process_id: str, variables: Dict) -> str:
    """Running a Zeebe instance.

    Args:
        client (ZeebeClient): Zeebe client
        bpmn_process_id (str): .bpmn file process id. Can be found in the .bpmn file.
        variables (Dict): Variables to start the instance with.

    Returns:
        str: Success or error message.
    """
    try:
        workflow_instance_key = client.run_workflow(bpmn_process_id=bpmn_process_id, variables=variables)
        success_msg = f"Instance now running with workflow instance key: {workflow_instance_key}"
        logger.info(success_msg)
        return success_msg
    except Exception as e:
        error_response_dict = {
            "code": str(e.__context__.code()),
            "details": e.__context__.details(),
            "debug_string": json.loads(e.__context__.debug_error_string()),
        }
        logger.error(error_response_dict)
        return error_response_dict


def publish_message_module(client: ZeebeClient, messag_name: str, correlation_key: str, variables: Dict) -> str:
    """Function for publishing message.

    Args:
        client (ZeebeClient): Zeebe client.
        messag_name (str): The name of the message.
        correlation_key (str): The chosen correlation_key.
        variables (Dict): Variables to publish with the message.

    Returns:
        str: Success or error message.
    """
    try:
        client.publish_message(name=messag_name, correlation_key=correlation_key, variables=variables)
        success_msg = "Message was published successfully!"
        logger.info(success_msg)
        return success_msg
    except Exception as e:
        if type(e).__name__ == "TypeError":
            logger.error(str(e))
            return str(e)
        else:
            error_response_dict = {
                "code": str(e.__context__.code()),
                "details": e.__context__.details(),
                "debug_string": json.loads(e.__context__.debug_error_string()),
            }
            logger.error(error_response_dict)
            return error_response_dict
