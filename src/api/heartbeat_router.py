from fastapi import APIRouter
import json
import logging
from google.protobuf.json_format import MessageToDict
from zeebe_grpc.gateway_pb2 import TopologyRequest

from ..zeebe.tasks import worker


logger = logging.getLogger()

router = APIRouter()


@router.get("/version")
async def version():
    try:
        return {
            "zeebe": {"broker": MessageToDict(worker.zeebe_adapter._gateway_stub.Topology(TopologyRequest()))}
        }

    except Exception as e:
        error_response_dict = {
            "code": str(e.code()),
            "details": e.details(),
            "debug_string": json.loads(e.debug_error_string()),
        }
        logger.error(error_response_dict)
        return error_response_dict
