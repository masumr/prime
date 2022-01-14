from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework.fields import SerializerMethodField

from apis_client.mixins.mixin_profile import MixinOwnProfileSerializer
from models.models import Profile, Producer


class OwnProfileSerializer(DynamicModelSerializer, MixinOwnProfileSerializer):
    total_sales = SerializerMethodField()
    
    @staticmethod
    def get_total_sales(profile: Profile):
        try:
            return profile.producer.get_total_sales()
        except Producer.DoesNotExist:
            return 0
    
    class Meta:
        model = Profile
        fields = Profile.public_fields + ('total_sales',)
        read_only_fields = Profile.read_only_fields
        deferred_fields = ('total_sales',)
