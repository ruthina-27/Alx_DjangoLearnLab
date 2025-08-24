from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    target_type = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'actor_username', 'verb', 'target_type', 'timestamp', 'read']
    
    def get_target_type(self, obj):
        if obj.target:
            return obj.target.__class__.__name__.lower()
        return None
