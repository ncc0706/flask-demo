"""
    #: Default configuration parameters.
    default_config = ImmutableDict({
        'DEBUG':                                get_debug_flag(default=False),
        'TESTING':                              False,
        'PROPAGATE_EXCEPTIONS':                 None,
        'PRESERVE_CONTEXT_ON_EXCEPTION':        None,
        'SECRET_KEY':                           None,
        'PERMANENT_SESSION_LIFETIME':           timedelta(days=31),
        'USE_X_SENDFILE':                       False,
        'LOGGER_NAME':                          None,
        'LOGGER_HANDLER_POLICY':               'always',
        'SERVER_NAME':                          None,
        'APPLICATION_ROOT':                     None,
        'SESSION_COOKIE_NAME':                  'session',
        'SESSION_COOKIE_DOMAIN':                None,
        'SESSION_COOKIE_PATH':                  None,
        'SESSION_COOKIE_HTTPONLY':              True,
        'SESSION_COOKIE_SECURE':                False,
        'SESSION_REFRESH_EACH_REQUEST':         True,
        'MAX_CONTENT_LENGTH':                   None,
        'SEND_FILE_MAX_AGE_DEFAULT':            timedelta(hours=12),
        'TRAP_BAD_REQUEST_ERRORS':              False,
        'TRAP_HTTP_EXCEPTIONS':                 False,
        'EXPLAIN_TEMPLATE_LOADING':             False,
        'PREFERRED_URL_SCHEME':                 'http',
        'JSON_AS_ASCII':                        True,
        'JSON_SORT_KEYS':                       True,
        'JSONIFY_PRETTYPRINT_REGULAR':          True,
        'JSONIFY_MIMETYPE':                     'application/json',
        'TEMPLATES_AUTO_RELOAD':                None,
    })
"""

import os

ENV = 'develop'
DEBUG = True
SECRET_KEY = os.urandom(24)
SESSION_COOKIE_NAME = 'flask_session'

# =======================================================
# database
# =======================================================
DATABASES = {
    'default': {
        'HOST': '',
        'ENGINE': 'sqlite3',
        'PORT': '',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
    },
}

# =======================================================
# bcrypt
# =======================================================
BCRYPT_LOG_ROUNDS = 4  # For faster tests; needs at least 4 to avoid "ValueError: Invalid rounds"

# =======================================================
# debug_tool_bar
# =======================================================
DEBUG_TB_ENABLED = False  # Disable Debug toolbar
DEBUG_TB_INTERCEPT_REDIRECTS = False

# =======================================================
# cache
# =======================================================
CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

# =======================================================
# sqlalchemy
# =======================================================
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False

# =======================================================
# webpack
# =======================================================
WEBPACK_MANIFEST_PATH = 'webpack/manifest.json'

# =======================================================
# csrf
# =======================================================
WTF_CSRF_ENABLED = False  # Allows form testing

# =======================================================
# celery
# =======================================================
CELERY_BORKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_IMPORTS = ('common.tasks',)