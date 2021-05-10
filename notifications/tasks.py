from celery.decorators import task
from celery.utils.log import get_task_logger
import notifications.utils as utils


logger = get_task_logger(__name__)


@task
def send_email():
    logger.info(f"Sent emails")
    utils.send_email_notifications()
