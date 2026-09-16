from django.urls import path
from . import views

urlpatterns = [
    path('',views.comparateur, name='comparateur'),
]
