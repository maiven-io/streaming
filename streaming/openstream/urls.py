from django.urls import path
from . import views

urlpatterns = [
    path('create-thread/', views.create_thread, name='create_thread'),
    path('add-message/', views.add_message, name='add_message'),
    path('run-assistant/', views.run_assistant, name='run_assistant'),
    path('stream-assistant/<str:thread_id>/', views.start_stream_run, name='stream_assistant'),  # Stream responses


]


