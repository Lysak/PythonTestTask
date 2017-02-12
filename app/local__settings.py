DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'product_db',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

SECRET_KEY = 'wn*shrs0+4m7y4fiv8nt&b$9_by!p0-7clo#50v7+8am(ae5t%'


