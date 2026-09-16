from notifications.models import Notification

def notification_count(request):

   notifications_non_lues = 0
   if request.user.is_authenticated:

        notifications_non_lues = (
            Notification.objects.filter(
                utilisateur=request.user,
                lu=False
            ).count()
        )

   return {

        'notifications_non_lues':
            notifications_non_lues

    }
