from pyramid.config import Configurator
from pyramid.events import subscriber
from pyramid.events import NewRequest

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid_beaker import session_factory_from_settings
from pyramid_beaker import set_cache_regions_from_settings
from .security import groupfinder

import pymongo
from innovation.resources import Root

def main(global_config, **settings):

  authn_policy = AuthTktAuthenticationPolicy('sosecret', callback=groupfinder)
  authz_policy = ACLAuthorizationPolicy()
  session_factory = session_factory_from_settings(settings)
  set_cache_regions_from_settings(settings)

  config = Configurator(
    settings=settings, 
    root_factory= 'innovation.models.RootFactory',
    authentication_policy=authn_policy,
    authorization_policy=authz_policy,
    session_factory=session_factory
  )  
  
  # Business owner / employee routes
  config.add_route('root', '/')
  config.add_route('login', '/login')
  config.add_route('logout', '/logout')
  config.add_route('add_employee', '/manage/employees/add')
  config.add_route('manage_employees', '/manage/employees')
  config.add_route('manage_all', '/manage')
  config.add_route('manage', '/manage/{b_id}')
  config.add_route('get_queue', '/get_queue')
  config.add_route('remove_from_queue', '/remove')
  config.add_route('add_to_queue_manual', '/add_to_queue_manual')
  config.add_route('notify_user', '/notify_user')
  config.add_route('check_in', '/check_in')
  config.add_route('check_out', '/check_out')

  # Admin routes
  config.add_route('admin_main', '/admin')
  config.add_route('admin_list_business', '/admin/business')
  config.add_route('admin_edit_business', '/admin/business/edit')
  config.add_route('admin_add_business', '/admin/business/add')
  config.add_route('admin_list_user', '/admin/user')
  config.add_route('admin_add_user', '/admin/user/add')
  config.add_route('admin_edit_user', '/admin/user/edit')
  #config.add_route('', '')

  config.add_static_view('static', 'innovation:static')

  # MongoDB
  def add_mongo_db(event):
        settings = event.request.registry.settings
        url = settings['mongodb.url']
        db_name = settings['mongodb.db_name']
        db = settings['mongodb_conn'][db_name]
        event.request.db = db
  db_uri = settings['mongodb.url']
  MongoDB = pymongo.Connection
  if 'pyramid_debugtoolbar' in set(settings.values()):
        class MongoDB(pymongo.Connection):
            def __html__(self):
                return 'MongoDB: <b>{}></b>'.format(self)
  conn = MongoDB(db_uri)
  config.registry.settings['mongodb_conn'] = conn
  config.add_subscriber(add_mongo_db, NewRequest)
  config.scan('innovation')
  return config.make_wsgi_app()
