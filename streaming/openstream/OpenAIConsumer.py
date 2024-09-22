from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache
import json

class OpenAIConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.thread_id = self.scope['url_route']['kwargs']['thread_id']
        print(f"Thread ID from WebSocket URL: {self.thread_id}")

        self.group_name = f"thread_{self.thread_id}"

        # Join WebSocket group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        print(f"WebSocket disconnected with code {close_code}")
        # Leave WebSocket group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    # Handle messages received from WebSocket (frontend)
    async def receive(self, text_data):
        print(f"Received message: {text_data}")

        # Parse the received message from the frontend
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')

        # Optionally process the message or broadcast it to other clients here
        # For now, we'll echo the message back to the client as a test
        await self.send(text_data=json.dumps({
            'message': f"Echo from server: {message}"
        }))

    # Receive a message from Redis cache and broadcast it to the WebSocket
    async def send_cached_message(self, event):
        cached_messages = cache.get(self.thread_id, "")
        await self.send(text_data=cached_messages)


    async def stream_message(self, event):
        message = event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({'message': message}))