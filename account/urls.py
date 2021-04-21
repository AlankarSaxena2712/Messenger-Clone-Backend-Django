from django.urls import path

from .views import *

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginAPIView.as_view()),
    path('room', RoomAPIView.as_view()),
    path('message/<slug:room>', MessageAPIView.as_view()),
]

