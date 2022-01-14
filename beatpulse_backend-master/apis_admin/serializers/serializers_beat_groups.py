from django.utils.text import slugify
from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.fields import SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from analytics_module.models import BeatPlay
from apis_client.mixins.mixin_beat_group import MixinBeatGroupSerializer
from apis_client.serializers.serializer_beat import BeatSerializer
from models.models import Playlist, Genre, Mood, FollowedPlaylist

_common_serializer_fields = ('image_thumbnail_file_path', 'image_background_file_path')


class _AbstractBeatGroupSerializer(MixinBeatGroupSerializer, DynamicModelSerializer):
    # they should in the mixin
    number_of_beats = SerializerMethodField()
    
    def create(self, validated_data):
        instance = super().create(dict(**validated_data, slug=slugify(validated_data['name'])))
        return instance
    
    def update(self, instance, validated_data):
        if 'name' in validated_data:
            # add the slugified name
            validated_data = dict(**validated_data, slug=slugify(validated_data['name']))
        instance = super().update(instance, validated_data)
        return instance


class PlaylistSerializer(_AbstractBeatGroupSerializer):
    number_of_followers = SerializerMethodField()
    number_of_plays = SerializerMethodField()
    beats = DynamicRelationField(BeatSerializer, embed=True, many=True)

    @staticmethod
    def get_number_of_followers(playlist: Playlist):
        return playlist.followedplaylist_set.count()

    @staticmethod
    def get_number_of_plays(playlist: Playlist):
        return BeatPlay.objects.filter(beat__in=playlist.beats.all()).count()
    
    class Meta:
        model = Playlist
        fields = Playlist.public_fields + _common_serializer_fields + ('date_of_creation', 'number_of_plays')
        deferred_fields = ('beats', 'number_of_plays')
        extra_kwargs = {
            'tagged_file_path': {'image_thumbnail_file_path': True},
            'mp3_file_path': {'image_background_file_path': True},
        }


class GenreSerializer(_AbstractBeatGroupSerializer):
    beats = DynamicRelationField(BeatSerializer, embed=True, many=True)
    # they should in the mixin
    number_of_beats = SerializerMethodField()

    @staticmethod
    def get_number_of_beats(group):
        return group.beats.filter(is_published=True).count() + group.subgenre_beats.filter(is_published=True).count()
    
    class Meta:
        model = Genre
        fields = Genre.public_fields + _common_serializer_fields + ('order_position',)
        deferred_fields = ('beats',)
        extra_kwargs = {
            'tagged_file_path': {'image_thumbnail_file_path': True},
            'mp3_file_path': {'image_background_file_path': True},
        }


class MoodSerializer(_AbstractBeatGroupSerializer):
    beats = DynamicRelationField(BeatSerializer, embed=True, many=True)
    
    class Meta:
        model = Mood
        fields = Mood.public_fields + _common_serializer_fields + ('order_position',)
        deferred_fields = ('beats',)
        extra_kwargs = {
            'tagged_file_path': {'image_thumbnail_file_path': True},
            'mp3_file_path': {'image_background_file_path': True},
        }
