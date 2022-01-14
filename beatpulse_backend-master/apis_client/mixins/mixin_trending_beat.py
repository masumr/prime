from models.models import TrendingBeat


class MixinTrendingBeatViewset:
    queryset = TrendingBeat.objects.all()


class MixinTrendingBeatSerializer:
    class Meta:
        model = TrendingBeat
        fields = '__all__'
