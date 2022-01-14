from django.db.models import Count
from dynamic_rest.fields import SerializerMethodField

from amazons3_module.cloudfront import CLOUDFRONT_URL
from models.models import Producer, Beat, FollowedProducer


class MixinProducerSerializer:
    # number_of_followers = SerializerMethodField()
    # number_of_beats = SerializerMethodField()
    
    @staticmethod
    def get_number_of_followers(producer: Producer):
        return producer.followedproducer_set.count()
    
    @staticmethod
    def get_number_of_beats(producer: Producer):
        return producer.beat_set.filter(is_published=True).count()
