from abc import abstractmethod
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from rest_framework.views import APIView

from analytics_module.consts import PERIOD_LAST_MONTH, PERIOD_LAST_SIX_MONTHS, PERIOD_ALL_TIME
from apis_admin.permissions.permissions import IsDashboardUser


class _Dates:
    def __init__(self):
        self.now = datetime.now().date()
        current_day = self.now.day
        # the days of the current month
        self.this_month_days = [self.now - timedelta(days=current_day - x - 1) for x in range(current_day)]
        # self.last_30_days = [now - timedelta(days=29 - x) for x in range(30)]
        # one day per month of last 6 months
        self.last_6_months_by_month = [self.now - relativedelta(months=5 - x) for x in range(6)]
        # the start of the month before current one
        self.start_of_month_before = self.now - relativedelta(months=1)
        self.start_of_month_before.replace(day=1)
        # self.one_month_ago = now - relativedelta(months=1)
        # self.two_months_ago = now - relativedelta(months=2)
        # today but 6 months ago
        self.six_months_ago = self.now - relativedelta(months=6)
        self.twelve_months_ago = self.now - relativedelta(months=12)
        self.first_date_possible = datetime(1970, 1, 1).date()


class _TotalData:
    def __init__(self, function_to_get_data):
        dates = _Dates()
        
        self.last_month = function_to_get_data(from_date=dates.this_month_days[0], to_date=dates.now)
        month_before = function_to_get_data(from_date=dates.start_of_month_before,
                                            to_date=dates.this_month_days[0] - timedelta(days=1))
        self.change_last_month = self._get_change_percentage(month_before, self.last_month)
        
        self.last_six_months = function_to_get_data(from_date=dates.six_months_ago, to_date=dates.now)
        six_months_before_last_six_months = function_to_get_data(from_date=dates.twelve_months_ago, to_date=dates.six_months_ago - timedelta(days=1))
        self.change_six_months = self._get_change_percentage(six_months_before_last_six_months, self.last_six_months)
        
        self.all_time = function_to_get_data(from_date=dates.first_date_possible, to_date=dates.now)
    
    @staticmethod
    def _get_change_percentage(current_value, previous_value):
        """
        returns the change in % from two values
        """
        if previous_value is None or current_value is None or current_value == 0:
            return 0
        return (previous_value - current_value) / current_value * 100
    
    def to_json(self):
        return {
            PERIOD_LAST_MONTH: self.last_month,
            'change_last_month': self.change_last_month,
            PERIOD_LAST_SIX_MONTHS: self.last_six_months,
            'change_six_months': self.change_six_months,
            PERIOD_ALL_TIME: self.all_time
        }


class _DetailData:
    def __init__(self, function_to_get_data_for_day, function_to_get_data_for_month):
        dates = _Dates()
        
        self.by_days = [function_to_get_data_for_day(x) for x in dates.this_month_days]
        self.by_months = [function_to_get_data_for_month(x) for x in dates.last_6_months_by_month]
    
    def to_json(self):
        return {
            'by_days': self.by_days,
            'by_months': self.by_months,
        }


class TotalView(APIView):
    permission_classes = (IsDashboardUser,)
    
    @abstractmethod
    def function_to_get_data(self, from_date, to_date):
        pass
    
    def get(self, request, *args, **kwargs):
        return JsonResponse(_TotalData(function_to_get_data=self.function_to_get_data).to_json())


class DetailedView(APIView):
    permission_classes = (IsDashboardUser,)
    
    @abstractmethod
    def function_to_get_data_for_day(self, day):
        pass
    
    @abstractmethod
    def function_to_get_data_for_month(self, day):
        pass
    
    def get(self, request, *args, **kwargs):
        return JsonResponse(_DetailData(function_to_get_data_for_day=self.function_to_get_data_for_day,
                                        function_to_get_data_for_month=self.function_to_get_data_for_month).to_json())
