# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
import os

from settings.settings_base import BASE_DIR

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = (
    os.path.join(BASE_DIR, 'staticfiles')
)
