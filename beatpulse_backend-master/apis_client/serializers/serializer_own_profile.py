from dynamic_rest.fields import SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer

from apis_client.mixins.mixin_profile import MixinOwnProfileSerializer
from models.models import Profile


class OwnProfileSerializer(DynamicModelSerializer, MixinOwnProfileSerializer):
    is_social = SerializerMethodField()
    
    @staticmethod
    def get_is_social(profile: Profile):
        return profile.is_social()
    
    class Meta:
        model = Profile
        fields = Profile.public_fields + ('is_social',)
        read_only_fields = Profile.read_only_fields + ('is_social',)
