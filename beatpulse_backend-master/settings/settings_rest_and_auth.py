AUTH_USER_MODEL = 'models.Profile'

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_ADAPTER = 'rest_auth_module.account_adapter.CustomUserAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'rest_auth_module.account_adapter.CustomSocialAdapter'
# it's mandatory to confirm the mail in order to activate
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7
# ACCOUNT_EMAIL_VERIFICATION = "optional"
DEFAULT_FROM_EMAIL = 'no-reply@beatpulse.app'


def ACCOUNT_USER_DISPLAY(user): return user.first_name


# no prefix in the subject of the mails
ACCOUNT_EMAIL_SUBJECT_PREFIX = ""
# uncomment below if want to test E-mails in console
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    # 'django.contrib.auth.backends.ModelBackend',
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_AUTH_REGISTER_SERIALIZERS = {
    # 'REGISTER_SERIALIZER': 'rest_auth_module.serializers.RegistrationSerializer',
}

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER': 'rest_auth_module.serializers.CustomPasswordResetSerializer',
}

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'dynamic_rest.renderers.DynamicBrowsableAPIRenderer',
    ],
}

DYNAMIC_REST = {
    'ENABLE_LINKS': False,
}


SOCIALACCOUNT_PROVIDERS = {
    "apple": {
        "APP": {
            # Your service identifier.
            "client_id": "app.beatpulse",

            # The Key ID (visible in the "View Key Details" page).
            "secret": "VVM7YT9X5S",

             # Member ID/App ID Prefix -- you can find it below your name
             # at the top right corner of the page, or it’s your App ID
             # Prefix in your App ID.
            "key": "RM4TSSA9PD",

            # The certificate you downloaded when generating the key.
            "certificate_key": """-----BEGIN PRIVATE KEY-----
MIGTAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBHkwdwIBAQQg5ueRCEdMZxwBmng4
ByEqCkO8CN34RNJOyV0uptbv0aGgCgYIKoZIzj0DAQehRANCAAR4CkjzbRwHaDpT
m8jpvDL2YxEdXPKVT1XjlWkqG6UKX5RX84/IwZIX1JMAA/khY9D64kA8Dk0VIPVa
PnFkB4E/
-----END PRIVATE KEY-----
"""
        }
    }
}