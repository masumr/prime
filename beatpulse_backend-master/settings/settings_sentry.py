import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

from settings.settings_base import DEBUG

if not DEBUG:
    sentry_sdk.init(
        dsn="https://b1ecb522170f4470a427b69b14672629@o224002.ingest.sentry.io/5216823",
        integrations=[DjangoIntegration()],
        
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'django.log',
                'formatter': 'verbose',
            },
            'mail_admins': {
                'level': 'ERROR',
                'class': 'django.utils.log.AdminEmailHandler',
                'include_html': True
            }
        },
        'formatters': {
            'verbose': {
                'format': '%(asctime)s %(levelname)-8s [%(name)s:%(lineno)s] %(message)s',
            },
        },
        'loggers': {
            '': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'django.security': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
        },
    }
