from django.urls import path

from tasks_module.views import check_for_abandoned_cart, update_trending_beats, delete_old_pending_orders

urlpatterns = [
    path('update_trending_beats/', update_trending_beats),
    path('check_for_abandoned_cart/', check_for_abandoned_cart),
    path('delete_old_pending_orders/', delete_old_pending_orders),
]
