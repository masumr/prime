from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import AccountInvitation, Producer, Profile


class AccountInvitationSerializer(DynamicModelSerializer):
    
    @staticmethod
    def validate_email_sent_to(value: str):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError('There is already a profile with that email')
        return value
    
    class Meta:
        model = AccountInvitation
        fields = AccountInvitation.public_fields
        read_only_fields = ('token',)
