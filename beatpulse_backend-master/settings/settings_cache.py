from settings.settings_base import DEBUG, PRODUCTION

if not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
            'KEY_PREFIX': 'beatpulse' if PRODUCTION else 'test-beatpulse'
        }
    }
