import logging
from pyzeebe import Job

logger = logging.getLogger()


def log_decorator(job: Job) -> Job:
    """A decorator function used for logging tasks.

    Args:
        job (Job): Job/task.

    Returns:
        Job: Job/task.
    """
    if not hasattr(job, "_stat"):
        job._stat = "Initialized"
    else:
        job._stat = "Complete"
    logger.info(
        f"Job Type: {job.type}, Status: {job._stat}, Instance key: {job.workflow_instance_key}, Job key: {job.key}"
    )
    return job


def error_handler(exception: Exception, job: Job) -> None:
    """Error handler function for raising/handling task related exceptions.

    Args:
        exception (Exception): Exception raised in the task.
        job (Job): The job/task.
    """
    response = f"Job Type: {job.type}, Status: Failed, Instance key: {job.workflow_instance_key}, Job key: {job.key}, Error: {str(exception)}"
    logger.error(response, exc_info=True)
    if type(exception).__name__ == "ConnectionError":
        job.set_failure_status(response)
    else:
        job.set_error_status(response)
