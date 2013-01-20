from pyramid.httpexceptions import (
  HTTPFound,
  HTTPNotFound,
  )
from pyramid.view import (
  view_config,
  forbidden_view_config,
  )
from pyramid.security import (
  Allow,
  Authenticated,
  authenticated_userid,
  forget,
  remember,
  )
from .security import USERS  
from .models import User, Client
import datetime
from pyramid.response import Response
from pymongo.errors import InvalidId
from bson.objectid import ObjectId
from pyramid.url import route_url
from pyramid.renderers import render_to_response
import json


def get_all_businesses(request):
  b_list = []
  organizations = request.db['organizations'].find()
  for organization in organizations:
    b_list.append({'name' : organization['name'], '_id' : organization['_id'] })
  return b_list  

# Administrator overview panel
@view_config(route_name='admin_main', renderer='main.mako', permission='administrators')
def admin_main(request):
  return dict(
    logged_in=authenticated_userid(request)
  )
  
@view_config(route_name='admin_edit_user', renderer='admin_user_add_edit.mako', permission='administrators')
def admin_user_edit(request):
  b_list = get_all_businesses(request)
  return dict(
    b_list=b_list,
    logged_in=authenticated_userid(request)
  )
  
@view_config(route_name='admin_add_user', renderer='string', permission='administrators')
def admin_user_add(request):
  if request.method == 'POST':
    if not all(k in request.POST for k in ('employees[]', 'name', 'p_word', 'owners[]', 'permissions[]')):
      return "NO"
    name = request.POST['name']  
    password = request.POST['p_word']  
    permissions = []
    owner = []
    employee = []
    for k, v in request.POST.iteritems():
      if k == 'permissions[]':
        permissions.append(v)
      elif k == 'owners[]':
        owner.append(v)
      elif k == 'employees[]':
        employee.append(v)
    New_User = User(name, password, permissions)    
    New_User._add_groups(request, owner, employee)
    if New_User.save(request):
      return "OK"
    return "NO"  

  
@view_config(route_name='admin_add_business', renderer='admin_business_add_edit.mako', permission='administrators')
def admin_business_add(request):
  pass
  
@view_config(route_name='admin_edit_business', renderer='admin_business_add_edit.mako', permission='administrators')
def admin_business_edit(request):
  pass
  
