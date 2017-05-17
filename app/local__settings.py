DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '5427',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = 'wn*shrs0+4m7y4fiv8nt&b$9_by!p0-7clo#50v7+8am(ae5t%'

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
