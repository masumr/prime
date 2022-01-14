from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include

from apis_admin import urls_api as urls_api_admin
from apis_client import urls_api as urls_api_client
from apis_client.views import FacebookLogin, GoogleLogin,AppleLogin

urlpatterns = [
    path('admin/', admin.site.urls),
    # urls for apis
    path('api/', include(urls_api_client.router.urls)),
    path('api/', include('apis_client.urls')),
    path('api_admin/', include(urls_api_admin.router.urls)),
    path('api_admin/', include('apis_admin.urls')),
    # used by django rest framework
    # TODO: understand if it is needed
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # all auth
    # TODO: understand if it is needed
    path('accounts/', include('allauth.urls')),
    # for a custom reset password html
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),
    path('rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('rest-auth/apple/', AppleLogin.as_view(), name='apple_login'),
    path('s3/', include('amazons3_module.urls')),
    path('transloadit/', include('transloadit_module.urls')),
    path('sendgrid/', include('email_module.urls')),
    path('payment/', include('payment_module.urls')),
    path('firebase/', include('firebase_module.urls')),
    path('pdf/', include('pdf_module.urls')),
    path('tasks/', include('tasks_module.urls')),
    path('analytics/', include('analytics_module.urls')),
    # this url is used to generate email content for the password reset
    path('password-reset/<str:uidb64>/<str:token>',
         lambda request: HttpResponse("Hello world"),
         name='password_reset_confirm')
]
