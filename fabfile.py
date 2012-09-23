from fabric.api import *
from bars.settings import FABRIC_HOSTS, FABRIC_ENV

env.hosts = FABRIC_HOSTS

def prod():
  
  stop_fcgi()
  
  with cd('~/bars'):
    pull()
    with virtualenv(FABRIC_ENV):
      migrate_db()
      start_fcgi()
  restart_lighttpd()

def virtualenv(name='django'):
  '''
  Source a virtualenv on prefix
  '''
  return prefix('source ~/%s/bin/activate' % name)

def pull():
  '''
  Pull from github
  '''
  run('git pull origin master')

def migrate_db():
  '''
  Update db using South migrations
  '''
  run('./manage.py migrate geo')
  run('./manage.py migrate places')
  run('./manage.py migrate products')

def stop_fcgi(pidfile='bars.pid'):
  '''
  Kill the fast cgi process
  '''
  with settings(warn_only=True):
    output = run('kill -9 `cat %s`' % pidfile)
    if output.failed:
      print 'No pid found, server not stopped.'
      return
    run('rm %s' % pidfile)

def start_fcgi(pidfile='bars.pid'):
  '''
  Start the fast cgi process
  '''
  run('./manage.py runfcgi workdir=~/bars protocol=scgi pidfile=~/bars.pid host=localhost port=8200 outlog=~/cgi-bars-out.log errlog=~/cgi-bars-err.log')

def restart_lighttpd():
  '''
  Restart lighttpd
  '''
  pass
