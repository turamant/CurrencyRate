
from django.contrib import admin
from django.urls import path, include

from parser.views import apiView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('parser.urls')),
    path('api/', apiView, name='json')


]
