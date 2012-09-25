# Scrapy settings for scrapper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
import imp, os

BOT_NAME = 'bars-scrapper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scrapper.spiders']
NEWSPIDER_MODULE = 'scrapper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

# Super useful, permits to limit encoding sued
# Necessary for OS X and its dummy lxml2 package
ENCODING_ALIASES = {
  'iso-8859-1': 'iso-8859-1',
}

ITEM_PIPELINES = ['scrapper.pipelines.PlacePipeline']

DJANGO_USER_ID = 2

MY_ENV_PATH = os.path.realpath('../../virtualenv/bars')
MY_APP_PATH = os.path.realpath('../bars')

try:
  from local_settings import *
except ImportError, e:
  pass

def setup_django_env(app_path, env_path):

  # Virtual env
  env_path = os.path.join(env_path, 'bin/activate_this.py')
  execfile(env_path, dict(__file__=env_path))

  from django.core.management import setup_environ
  f, filename, desc = imp.find_module('settings', [app_path])
  project = imp.load_module('settings', f, filename, desc)       

  setup_environ(project)

  # Add django project to sys.path
  import sys
  sys.path.append(os.path.abspath(os.path.join(app_path, os.path.pardir)))

setup_django_env(MY_APP_PATH, MY_ENV_PATH)
