from dynamic_rest.fields import SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer

from apis_client.mixins.mixin_beat_group import MixinBeatGroupSerializer
from models.models import Playlist, Genre, Mood


class _AbstractBeatGroupSerializer(MixinBeatGroupSerializer, DynamicModelSerializer):
    # they should in the mixin
    number_of_beats = SerializerMethodField()


class PlaylistSerializer(_AbstractBeatGroupSerializer):
    number_of_followers = SerializerMethodField()
    
    @staticmethod
    def get_number_of_followers(playlist: Playlist):
        return playlist.followedplaylist_set.count()
    
    class Meta:
        model = Playlist
        fields = Playlist.public_fields
        deferred_fields = ('beats',)


class GenreSerializer(_AbstractBeatGroupSerializer):
    # they should in the mixin
    number_of_beats = SerializerMethodField()

    @staticmethod
    def get_number_of_beats(group):
        return group.beats.filter(is_published=True).count() + group.subgenre_beats.filter(is_published=True).count()
    
    class Meta:
        model = Genre
        fields = Genre.public_fields
        deferred_fields = ('beats',)


class MoodSerializer(_AbstractBeatGroupSerializer):
    class Meta:
        model = Mood
        fields = Mood.public_fields
        deferred_fields = ('beats',)
