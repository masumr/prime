from decouple import config
    
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'beat_pulse',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'beat_pulse-db'
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config("DB_NAME"),
#         'USER': config("DB_USER", 'postgres'),
#         'PASSWORD': config("DB_PASSWORD"),
#         'HOST': config("DB_HOST", "localhost"),
#         'PORT': config("DB_PORT", "5432"),
#     }
# }


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': "postgres",
#         'USER': 'postgres',
#         'PASSWORD': 'password',
#         'HOST':  "localhost",
#         'PORT': "5432",
#     }
# }


# https://docs.djangoproject.com/en/2.0/ref/settings/#std:setting-CONN_MAX_AGE
# The lifetime of a database connection, in seconds.
# Use 0 to close database connections at the end of each request — Django’s historical behavior —
# and None for unlimited persistent connections.
# CONN_MAX_AGE = 60
