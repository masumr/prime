from django.urls import path

from apis_admin.views import add_new_dashboard_user

urlpatterns = [
    path('add_new_dashboard_user/', add_new_dashboard_user),
]
