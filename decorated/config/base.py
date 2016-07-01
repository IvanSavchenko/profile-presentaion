"""Base app settings.

This settings should not be connect somehow with env.
"""

from unipath import Path

SECRET_KEY = 'do-or-do-not-there-is-no-try-Yoda'
BASE_DIR = Path(__file__).ancestor(2)

# Upload settings.
UPLOAD_FOLDER = BASE_DIR.child('media')
UPLOAD_URL = '/media/'

# Static settings.
STATIC_FOLDER = BASE_DIR.child('static')
STATIC_URL = '/static/'

# Token auth settings.
SECURITY_TOKEN_AUTHENTICATION_HEADER = "User-Token"
WTF_CSRF_ENABLED = False

# Logging settings.
LOG_DEFAULT_FORMAT = '%(asctime)s; %(filename)s:%(lineno)d; %(message)s'

# Profiler settings.
PROFILERS_DIR = BASE_DIR.child('profilers')
PROFILER_FILE_NAME = 'app.prof'
