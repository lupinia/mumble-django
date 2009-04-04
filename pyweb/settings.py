# Django settings for mumble_django project.

#################################################################
#################################################################
##                                                             ##
##  The only setting you should alter is this path.            ##
##  Mumble-Django will try to auto-detect this value if it     ##
##  isn't set, which is the default. However, if this should   ##
##  not work as expected, et this to the path where you        ##
##  extracted Mumble-Django.                                   ##
##                                                             ##
MUMBLE_DJANGO_ROOT = None;                                     ##
##                                                             ##
##  For a basic installation, this is all you need to edit in  ##
##  this file, the rest will be handled automatically!         ##
##                                                             ##
#################################################################
##                                                             ##
##  DO NOT CHANGE ANYTHING ELSE IN THIS FILE UNLESS YOU KNOW   ##
##  WHAT YOU ARE DOING!                                        ##
##                                                             ##
#################################################################
#################################################################

# Default email address to send mails from.
DEFAULT_FROM_EMAIL = "webmaster@localhost"


ACCOUNT_ACTIVATION_DAYS = 30


from os.path import join, dirname, abspath

if not MUMBLE_DJANGO_ROOT:
	MUMBLE_DJANGO_ROOT = dirname(dirname(abspath(__file__)));

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = join( MUMBLE_DJANGO_ROOT, 'mumble-django.db3' )
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = join( MUMBLE_DJANGO_ROOT, 'htdocs' )

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u-mp185msk#z4%s(do2^5405)y5d!9adbn92)apu_p^qvqh10v'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'pyweb.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    join( MUMBLE_DJANGO_ROOT, 'template' ),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'registration',
    'mumble',
)