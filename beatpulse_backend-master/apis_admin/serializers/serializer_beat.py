from typing import List

from dynamic_rest.fields import SerializerMethodField
from dynamic_rest.serializers import DynamicModelSerializer
from rest_framework import serializers

from models.models import Beat, Genre, Mood, Playlist, BeatProducerRelation, Producer, BeatKey


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
        fields = ('profile', 'display_name', 'image_logo_url')


class _BeatProducerRelationSerializer(serializers.ModelSerializer):
    producer = _ProducerSerializer(read_only=True)
    producer_id = serializers.PrimaryKeyRelatedField(queryset=Producer.objects.all(), source='producer',
                                                     write_only=True)
    
    class Meta:
        model = BeatProducerRelation
        fields = ('producer', 'producer_id', 'commission')


class _PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name')


class _BeatKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = BeatKey
        fields = ('id', 'name')


class BeatSerializer(DynamicModelSerializer):
    genre = _GenreSerializer(read_only=True)
    genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='genre', write_only=True, allow_null=True)
    sub_genre = _GenreSerializer(read_only=True)
    sub_genre_id = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(), source='sub_genre', write_only=True, allow_null=True)
    mood = _MoodSerializer(read_only=True)
    mood_id = serializers.PrimaryKeyRelatedField(
        queryset=Mood.objects.all(), source='mood', write_only=True, allow_null=True)
    producers = _BeatProducerRelationSerializer(many=True)
    playlists = _PlaylistSerializer(many=True, read_only=True)
    playlists_ids = serializers.PrimaryKeyRelatedField(queryset=Playlist.objects.all(), source='playlists', many=True,
                                                       write_only=True)
    key = _BeatKeySerializer(read_only=True)
    key_id = serializers.PrimaryKeyRelatedField(
        queryset=BeatKey.objects.all(), source='key', write_only=True, allow_null=True)
    
    number_of_likes = SerializerMethodField()
    number_of_plays = SerializerMethodField()
    number_of_demo_downloads = SerializerMethodField()
    number_of_shares = SerializerMethodField()
    
    @staticmethod
    def get_number_of_likes(beat: Beat):
        return beat.likedbeat_set.count()
    
    @staticmethod
    def get_number_of_plays(beat: Beat):
        return beat.beatplay_set.count()
    
    @staticmethod
    def get_number_of_demo_downloads(beat: Beat):
        return beat.beatdemodownload_set.count()
    
    @staticmethod
    def get_number_of_shares(beat: Beat):
        return beat.beatshare_set.count()
    
    @staticmethod
    def _update_producers(instance: Beat, producers_with_commission: List[dict]):
        # delete old producers
        instance.producers.clear()
        # create new ones
        for x in producers_with_commission:
            BeatProducerRelation.objects.create(beat=instance, **x)
    
    def create(self, validated_data):
        producers_with_commission: List[dict] = validated_data.pop('producers')
        instance: Beat = super().create(validated_data)
        self._update_producers(instance, producers_with_commission)
        return instance
    
    def update(self, instance: Beat, validated_data):
        # some patch may not pass producers (when only the image is updated)
        producers_with_commission: List[dict] = validated_data.pop('producers') \
            if 'producers' in validated_data else []
        instance: Beat = super().update(instance, validated_data)
        # as above so below
        if len(producers_with_commission) > 0:
            self._update_producers(instance, producers_with_commission)
        return instance
    
    class Meta:
        model = Beat
        fields = Beat.public_fields + (
            'date_of_release', 'genre_id', 'sub_genre_id', 'mood_id', 'playlists_ids', 'key_id',
            'tagged_file_path', 'stream_file_path', 'mp3_file_path', 'wav_file_path', 'trackout_file_path',
            'image_file_path', 'image_thumbnail_file_path', 'is_published', 'number_of_likes', 'number_of_plays',
            'number_of_demo_downloads', 'number_of_shares', 'energy')
        deferred_fields = (
            'waveform_data', 'tags', 'number_of_likes', 'number_of_plays', 'number_of_demo_downloads',
            'number_of_shares')
        read_only_fields = ('image_url', 'image_thumbnail_url')
        extra_kwargs = {
            'image_file_path': {'write_only': True},
            'image_thumbnail_file_path': {'write_only': True},
        }
