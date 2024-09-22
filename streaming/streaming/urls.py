# streaming/urls.py (or your main project's urls.py)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('openstream/', include('openstream.urls')),  # Ensure this line is here
]
