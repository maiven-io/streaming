import json
from django.http import JsonResponse
from django.http import StreamingHttpResponse
from openai.types.beta.threads import TextDelta, Text
from celery import shared_task

from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
from openai import AssistantEventHandler
from .event_handlers import SimpleEventHandler

from typing_extensions import override
from .credentials_openai import OPENAI_API_KEY, ASSISTANT_ID, THREAD_ID
from openstream.tasks import SimpleEventHandler

from django.http import JsonResponse
from .tasks import stream_openai_response
from django.core.cache import cache
from celery.utils.log import get_task_logger
from .tasks import *


logger = get_task_logger(__name__)



# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
thread_id = THREAD_ID



@csrf_exempt
def create_thread(request):
    if request.method == 'POST':
        try:
            # Create a new thread with the Assistant
            thread = client.beta.threads.create(assistant_id=ASSISTANT_ID)

            # Return the created thread's ID
            return JsonResponse({
                'success': True,
                'thread_id': thread.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def add_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread_id = data.get('thread_id')
            content = data.get('content')

            if not thread_id or not content:
                return JsonResponse({'error': 'Thread ID and message content are required.'}, status=400)

            # Add a message to the thread
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )

            return JsonResponse({
                'success': True,
                'message_id': message.id
            }, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


@csrf_exempt
def run_assistant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            thread_id = data.get('thread_id')

            if not thread_id:
                return JsonResponse({'error': 'Thread ID is required.'}, status=400)

            # Execute a run on the specified thread and assistant
            run = client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=ASSISTANT_ID  # You can override model and instructions if needed
            )

            # Convert the response to a dictionary for JSON serialization
            run_data = run.to_dict()

            return JsonResponse({
                'success': True,
                'response': run_data
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)


def start_stream_run(request, thread_id, assistant_id):
    if request.method == 'POST':
        # Start the Celery task for streaming OpenAI responses
        stream_openai_response.delay(thread_id, assistant_id)
        return JsonResponse({"status": "Streaming started"})
    return JsonResponse({"error": "Invalid request method"}, status=400)


def get_stream_messages(request, thread_id):
    # Fetch the response from Redis cache
    cached_messages = cache.get(thread_id, "")
    return JsonResponse({"messages": cached_messages.split('\n')})

@csrf_exempt
def test_openai_stream(request):
    thread_id = request.POST.get('thread_id', 'default_thread_id')
    assistant_id = ASSISTANT_ID
    response_text = ""

    try:
        event_handler = SimpleEventHandler(thread_id)
        with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=event_handler
        ) as stream:
            stream.until_done()

        return JsonResponse({"response": event_handler.response_text})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def add_message_and_stream(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        thread_id = data.get('thread_id')
        content = data.get('content')

        if not thread_id or not content:
            return JsonResponse({'error': 'Thread ID and message content are required.'}, status=400)

        # Add a message to the thread
        try:
            message = client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=content
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Trigger the Celery task to start streaming in the background
        assistant_id = ASSISTANT_ID  # Ensure ASSISTANT_ID is available
        task = stream_openai_response.delay(thread_id, assistant_id)  # Call the Celery task

        # Respond immediately with task info
        return JsonResponse({
            'success': True,
            'message_id': message.id,
            'celery_task_id': task.id  # Return the task ID for tracking
        }, status=201)

    


def start_streaming(request, thread_id, assistant_id):
    try:
        logger.info(f"Received request to start streaming for thread {thread_id} with assistant {assistant_id}")
        
        # Call the Celery task to stream the response
        stream_openai_response.delay(thread_id, assistant_id)  # Use `.delay` to run asynchronously

        return JsonResponse({'status': 'Streaming started', 'thread_id': thread_id, 'assistant_id': assistant_id})

    except Exception as e:
        logger.error(f"Error in start_streaming view: {e}")
        return JsonResponse({'status': 'Error', 'message': str(e)}, status=500)