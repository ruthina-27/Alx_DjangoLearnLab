from django.urls import path
from .views import NotificationListView, mark_notification_read

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/<int:notification_id>/read/', mark_notification_read, name='mark-notification-read'),
]
