from settings.settings_base import PRODUCTION, DEBUG

TAGGED_FILE_TYPE = 'Tagged'
MP3_FILE_TYPE = 'MP3'
WAV_FILE_TYPE = 'WAV'
TRACKOUT_FILE_TYPE = 'Trackout'
BEATPULSE_COMMISSION_PERCENTAGE = 50.0
IP_INFO_TOKEN = '8af48c710ac20d'
APP_URL = 'https://beatpulse.app' if PRODUCTION else 'http://localhost:8080' if DEBUG else 'https://test.beatpulse.app'
APP_API_URL = 'https://api.beatpulse.app' if PRODUCTION else 'http://localhost:8000' if DEBUG else 'https://test-api.beatpulse.app'
