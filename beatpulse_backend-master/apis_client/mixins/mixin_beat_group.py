from models.models import Genre, Mood


class MixinGenreViewSet:
    queryset = Genre.objects.order_by('order_position')


class MixinMoodViewSet:
    queryset = Mood.objects.order_by('order_position')


class MixinBeatGroupSerializer:
    
    @staticmethod
    def get_number_of_beats(group):
        return group.beats.filter(is_published=True).count()

