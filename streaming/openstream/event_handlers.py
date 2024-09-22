# event_handlers.py
import logging
from django.core.cache import cache
from openai import AssistantEventHandler

logger = logging.getLogger(__name__)

class SimpleEventHandler(AssistantEventHandler):
    def __init__(self, thread_id):
        super().__init__()  # Properly initialize the base class
        self.thread_id = thread_id
        self.response_text = ""
        logger.info(f"Event handler initialized for thread {thread_id}")

    def on_text_created(self, text):
        self.response_text += text.value
        logger.info(f"Before caching text created for thread {self.thread_id}")
        cache.set(self.thread_id, self.response_text, timeout=60 * 60)
        logger.info(f"Text created: {text.value} | Cached response: {self.response_text}")

    def on_text_delta(self, delta, snapshot):
        self.response_text += delta.value
        logger.info(f"Before caching text delta for thread {self.thread_id}")
        cache.set(self.thread_id, self.response_text)
        logger.info(f"Text delta: {delta.value} | Cached response: {self.response_text}")

    def on_end(self):
        logger.info("Stream ended")
        self.response_text += "\n[Stream Ended]"
        logger.info(f"Before caching end response for thread {self.thread_id}")
        cache.set(self.thread_id, self.response_text)
        logger.info(f"Stream ended | Cached response: {self.response_text}")
