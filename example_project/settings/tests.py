from .base import *  # noqa
import dj_database_url



# In tests, compressor has a habit of choking on failing tests and masking
# the real error.
COMPRESS_ENABLED = False

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

DATABASES = {
    'default': dj_database_url.config(
        default='postgres://postgres@172.17.0.1/postgres', conn_max_age=600
    ),
}
