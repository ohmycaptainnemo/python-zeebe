from fastapi import FastAPI, File, UploadFile
from pyzeebe import ZeebeClient
import uvicorn
import os
import json
import logging

from src.settings import Zeebe

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
logger = logging.getLogger()

if __name__ == "__main__":

    client = ZeebeClient(hostname = Zeebe.ZEEBE_HOSTNAME, port = Zeebe.ZEEBE_PORT, max_connection_retries = Zeebe.ZEEBE_MAX_CONNECTION_RETRIES)

    app = FastAPI(docs_url="/")

    with open("VERSION", "r") as f:
        VERSION = f.read()

    @app.get("/version")
    def version():
        return VERSION
    
    @app.post("/deploy")
    def deploy_workflow(bpmn_file: UploadFile = File(...)):
        bpmn_file_path = os.path.join(Zeebe.BPMN_DUMP_PATH, bpmn_file.filename)
        try:
            logger.info("Started saving .bpmn file.")
            with open(bpmn_file_path, "wb+") as file_obj:
                file_obj.write(bpmn_file.file.read())
            logger.info(f'Finished saving .bpmn file. File is at {bpmn_file_path}')
        except IOError as e:
            logger.error("Could not open or write to the .bpmn file!")

        try:
            client.deploy_workflow(bpmn_file_path)
            success_msg = ".bpmn deployment was successful!" 
            logger.info(success_msg)
            return(success_msg)
        except Exception as e:
            error_response_dict = {
                "code": str(e.__context__.code()),
                "details": e.__context__.details(),
                "debug_string": json.loads(e.__context__.debug_error_string())
            }
            logger.error(error_response_dict)
            return(error_response_dict)

    @app.get("/run")
    def run_instance(bpmn_process_id: str):
        try:
            workflow_instance_key = client.run_workflow(bpmn_process_id= bpmn_process_id, variables={"orderId": "1"})
            success_msg = f'Instance now running with workflow instance key: {workflow_instance_key}' 
            logger.info(success_msg)
            return (success_msg) 
        except Exception as e:
            error_response_dict = {
                "code": str(e.__context__.code()),
                "details": e.__context__.details(),
                "debug_string": json.loads(e.__context__.debug_error_string())
            }
            logger.error(error_response_dict)
            return(error_response_dict)

    @app.get("/publish")
    def publish_message():
        try:
            client.publish_message(name = "mymsg", correlation_key = "1", variables = {"test": "Hello"})
            success_msg = "Message was published successfully!" 
            logger.info(success_msg)
            return (success_msg) 
        except Exception as e:
            if type(e).__name__ == "TypeError":
                logger.error(str(e))
                return(str(e))
            else:
                error_response_dict = {
                    "code": str(e.__context__.code()),
                    "details": e.__context__.details(),
                    "debug_string": json.loads(e.__context__.debug_error_string())
                }
                logger.error(error_response_dict)
                return(error_response_dict)


    uvicorn.run(app, host="0.0.0.0", port=5555)
