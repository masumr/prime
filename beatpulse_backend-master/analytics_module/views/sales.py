from dateutil.relativedelta import relativedelta
from django.db.models import Sum

from analytics_module.views.generic import TotalView, DetailedView
from models.models import Order, OrderItemIncome, ProducerPayout, Producer, OrderItem


class TotalSales(TotalView):
    def function_to_get_data(self, from_date, to_date):
        try:
            # if the request is made by the producer
            return OrderItem.objects \
                .filter(producer_incomes__producer=self.request.user.producer,
                        order__status=Order.STATUS_COMPLETE,
                        order__date__date__gte=from_date,
                        order__date__date__lte=to_date) \
                .aggregate(Sum('producer_incomes__income'))['producer_incomes__income__sum']
        except Producer.DoesNotExist:
            # if it is made by the admin
            return Order.objects.filter(status=Order.STATUS_COMPLETE,
                                        date__date__gte=from_date,
                                        date__date__lte=to_date) \
                .aggregate(Sum('total'))['total__sum']


class DetailedSales(DetailedView):
    def function_to_get_data_for_day(self, day):
        try:
            # if the request is made by the producer
            return OrderItem.objects \
                .filter(producer_incomes__producer=self.request.user.producer,
                        order__status=Order.STATUS_COMPLETE,
                        order__date__date=day) \
                .aggregate(Sum('producer_incomes__income'))['producer_incomes__income__sum']
        except Producer.DoesNotExist:
            # if it is made by the admin
            return Order.objects.filter(status=Order.STATUS_COMPLETE,
                                        date__date=day).aggregate(Sum('total'))['total__sum']
    
    def function_to_get_data_for_month(self, day):
        try:
            # if the request is made by the producer
            return OrderItem.objects \
                .filter(producer_incomes__producer=self.request.user.producer,
                        order__status=Order.STATUS_COMPLETE,
                        order__date__date__lte=day,
                        order__date__date__gt=day - relativedelta(months=1)) \
                .aggregate(Sum('producer_incomes__income'))['producer_incomes__income__sum']
        except Producer.DoesNotExist:
            # if it is made by the admin
            return Order.objects.filter(status=Order.STATUS_COMPLETE,
                                        date__date__lte=day,
                                        date__date__gt=day - relativedelta(months=1)) \
                .aggregate(Sum('total'))['total__sum']


class TotalNetSales(TotalView):
    def function_to_get_data(self, from_date, to_date):
        total_orders = Order.objects.filter(status=Order.STATUS_COMPLETE,
                                            date__date__gte=from_date,
                                            date__date__lte=to_date) \
            .aggregate(Sum('total'))['total__sum']
        producer_cut = OrderItemIncome.objects.filter(order_item__order__status=Order.STATUS_COMPLETE,
                                                      order_item__order__date__date__gte=from_date,
                                                      order_item__order__date__date__lte=to_date) \
            .aggregate(Sum('income'))['income__sum']
        
        if total_orders is None or producer_cut is None:
            return 0
        
        return total_orders - producer_cut


class TotalProducerPayouts(TotalView):
    def function_to_get_data(self, from_date, to_date):
        return ProducerPayout.objects \
            .filter(date__gte=from_date, date__lte=to_date) \
            .aggregate(Sum('payed_amount'))['payed_amount__sum']
