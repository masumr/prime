from django.db.models import Sum
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.fields import SerializerMethodField

from models.models import Profile, Order


class ProfileSerializer(DynamicModelSerializer):
    total_spent = SerializerMethodField()
    
    @staticmethod
    def get_total_spent(profile: Profile):
        return Order.objects.filter(status=Order.STATUS_COMPLETE,
                                    profile=profile).aggregate(Sum('total'))['total__sum']
    
    class Meta:
        model = Profile
        fields = Profile.public_fields + ('total_spent', 'platform', 'date_of_creation')
