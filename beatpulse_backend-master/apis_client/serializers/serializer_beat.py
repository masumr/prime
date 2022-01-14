from dynamic_rest.fields import DynamicRelationField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import Beat, Genre, Producer, Mood, Playlist, BeatKey


class _GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')


class _MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mood
        fields = ('id', 'name')


class _ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('profile', 'display_name')


class _PlaylistSerializer(DynamicModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name')


class _BeatKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatKey
        fields = ('name',)


class BeatSerializer(DynamicModelSerializer):
    genre = _GenreSerializer()
    sub_genre = _GenreSerializer()
    mood = _MoodSerializer()
    producers = _ProducerSerializer(many=True)
    playlists = DynamicRelationField(_PlaylistSerializer, embed=True, many=True)
    key = _BeatKeySerializer()
    
    class Meta:
        model = Beat
        fields = Beat.public_fields
        deferred_fields = ('playlists', 'waveform_data', 'tags')
