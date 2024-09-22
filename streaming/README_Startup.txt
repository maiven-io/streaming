we have redis server set up to manage cache for the stream.
we need to user WSL to start the server 
use command 

sudo service redis-server start

enter your password (admin for Tomek)


we also need to run Celery worker to manage the streaming 
use following in the terminal cd to your main app. you need to go directly to the folder with celery.py

you would need to have cd like streaming\streaming\streaming 

celery -A streaming worker  -E --loglevel=info


you will need to startup daphne/Channels: 
its to start the websocket server (daphne) to change websockets requests
you might need to cd \streaming

in terminal use: 

daphne -p 8001 streaming.asgi:application

port 8001 is used as django is using 8000 in this case

you need to start up your django project 

cd to streaming 

python manage.py runserver 


frontend startup is 

cd to streaming 
cd to frontend 

use: 
npm start



SHELL TESTS TO DO 


powershell invoke test to add message to a thread 

Invoke-WebRequest -Uri http://127.0.0.1:8000/openstream/add-message/ `
>>     -Method POST `
>>     -Headers @{"Content-Type"="application/json"} `
>>     -Body '{"thread_id": "thread_2nU1RPxlJ42nMYLuesE3I5xK", "content": "Hello, write for me a story about bears"}'


powershell invoke test to run thread: 


Invoke-WebRequest -Uri http://127.0.0.1:8000/openstream/run-assistant/ `
    -Method POST `
    -Headers @{"Content-Type"="application/json"} `
    -Body '{"thread_id": "thread_2nU1RPxlJ42nMYLuesE3I5xK"}'


Shell invoke to test if redis server is configured properly. use shell and inject 



from channels.layers import get_channel_layer
from asgiref.testing import ApplicationCommunicator
from channels.generic.websocket import AsyncWebsocketConsumer

# Create a dummy consumer to test connection
class TestConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="Connected")

channel_layer = get_channel_layer()

if channel_layer:
    print("Redis connection is configured properly.")
else:
    print("Redis connection is not configured.")




