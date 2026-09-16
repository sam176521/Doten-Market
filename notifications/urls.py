from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.mes_notifications,
        name='mes_notifications'
    ),

]
