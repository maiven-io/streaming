
from celery import shared_task
from openai import OpenAI
from django.core.cache import cache
from .event_handlers import SimpleEventHandler  # Import the event handler here
from .credentials_openai import OPENAI_API_KEY, THREAD_ID
import logging

client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger(__name__)
thread_id = THREAD_ID

@shared_task(bind=True)
def stream_openai_response(self, thread_id, assistant_id):
    try:
        logger.info(f"Streaming task started for thread {thread_id} with assistant {assistant_id}")
        logger.debug("Initializing the event handler and starting streaming...")
        # Initialize event handler with the thread_id
        event_handler = SimpleEventHandler(thread_id)
        logger.debug("Starting the streaming process...")
        
        # Start streaming
        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler
        ) as stream:
            logger.info(f"Started streaming for thread {thread_id}")
            stream.until_done()

        logger.info(f"Streaming completed for thread {thread_id}")

    except Exception as e:
        logger.error(f"Error in stream_openai_response task: {e}")
        self.retry(exc=e)
