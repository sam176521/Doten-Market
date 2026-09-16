from django.shortcuts import render
from notifications.models import Notification
from django.contrib.auth.decorators import login_required

@login_required
def mes_notifications(request):

    notifications = Notification.objects.filter(
        utilisateur=request.user,
        lu=False
    ).order_by('-date_creation')

    return render(
        request,
        'notifications/liste.html',
        {
            'notifications': notifications
        }
    )
# Create your views here.
