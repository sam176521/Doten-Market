from django.urls import path
from .views import home

urlpatterns = [
    path('',home,name='home'),
    path("test-media/", views.test_media, name="test_media"),
]
