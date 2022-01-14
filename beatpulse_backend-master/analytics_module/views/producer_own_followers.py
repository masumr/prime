from dateutil.relativedelta import relativedelta

from analytics_module.views.generic import TotalView, DetailedView
from models.models import FollowedProducer


class TotalProducerOwnFollowers(TotalView):
    def function_to_get_data(self, from_date, to_date):
        return FollowedProducer.objects.filter(producer=self.request.user.producer,
                                               date__gte=from_date,
                                               date__lte=to_date, ).count()


class DetailedProducerOwnFollowers(DetailedView):
    def function_to_get_data_for_day(self, day):
        return FollowedProducer.objects.filter(date=day, producer=self.request.user.producer).count()
    
    def function_to_get_data_for_month(self, day):
        return FollowedProducer.objects.filter(date__lte=day,
                                               date__gt=day - relativedelta(months=1),
                                               producer=self.request.user.producer).count()
