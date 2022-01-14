from dateutil.relativedelta import relativedelta

from analytics_module.views.generic import TotalView, DetailedView
from models.models import Profile


class TotalSignups(TotalView):
    def function_to_get_data(self, from_date, to_date):
        return Profile.objects.filter(date_of_creation__gte=from_date, date_of_creation__lte=to_date).count()


class DetailedSignups(DetailedView):
    def function_to_get_data_for_day(self, day):
        return Profile.objects.filter(date_of_creation=day).count()
    
    def function_to_get_data_for_month(self, day):
        return Profile.objects.filter(date_of_creation__lte=day,
                                      date_of_creation__gt=day - relativedelta(months=1)).count()
