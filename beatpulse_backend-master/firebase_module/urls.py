from django.urls import path

from firebase_module.views import share_link

urlpatterns = [
    path('share_link/<str:model>/<int:pk>/', share_link),
]
