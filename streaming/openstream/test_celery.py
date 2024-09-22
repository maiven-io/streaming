import json
from openai import OpenAI
from openstream.tasks import stream_openai_response
from django.core.cache import cache
from openstream.credentials_openai import OPENAI_API_KEY, ASSISTANT_ID

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Thread and Assistant IDs
thread_id = "thread_2nU1RPxlJ42nMYLuesE3I5xK"
assistant_id = "asst_Ibsbv3KtyxTuXB7lj88yVZOi"

# Send a message ("tell me a story about bears") to the existing thread
message_content = "tell me a story about bears"

try:
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message_content
    )
    print(f"Message ID: {message.id}")

    # Trigger the Celery task for streaming the response
    task = stream_openai_response.delay(thread_id, assistant_id)
    print(f"Triggered Celery task: {task.id}")

except Exception as e:
    print(f"Error: {str(e)}")
