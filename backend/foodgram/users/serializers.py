from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Users' serializer."""
    first_name = serializers.CharField(source='name')
    last_name = serializers.CharField(source='surname')
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')
        model = User

    def get_is_subscribed(self, obj):
        '''Checking if user is subscribed.'''
        if obj.follower.all():
            return True
        return False
