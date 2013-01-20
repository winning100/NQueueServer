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

@view_config(route_name='login', renderer='login.mako')
@view_config(route_name='root', renderer='login.mako')
@forbidden_view_config(renderer='login.mako')
def login_view(request):
  login_url = request.route_url('login')
  referrer = request.url
  if referrer == login_url: referrer = '/manage' 
  came_from = request.params.get('came_from', referrer)
  message = ''
  login = ''
  password = ''
  if 'form.submit' in request.params:
    login = request.params['login']
    password = request.params['password']
    New_User = User(login, password, None)
    if New_User.authenticate(request):
      headers = remember(request, login)
      session = request.session
      session['u_id'] = New_User._id
      return HTTPFound(location = came_from, headers = headers)
    message = 'Failed login'

  return dict(
    message = message, url = request.application_url + '/login',
    came_from = came_from, login = login, password = password,
    ) 

@view_config(route_name='logout')
def logout_view(request):
  headers = forget(request)
  loc = request.route_url('login')
  return HTTPFound(location=loc, headers=headers)

@view_config(route_name='manage', renderer='new_queue.mako', permission='b_queuers')
def manage_queue(request):
  b_id = request.matchdict['b_id']
  return dict(
    b_name='Test',
    b_id=b_id,
    logged_in=authenticated_userid(request)
  )

@view_config(route_name='get_queue', renderer='string')
def get_queue(request):
  if "_id" not in request.POST: print "Invalid request"
  b_id = request.POST['_id']
  organization= request.db['organizations'].find_one({'_id' : ObjectId(b_id)})
  raw = ""
  remove = '<a href="#" class="delete" onclick="delete_row(this)">Remove</a>'
  notify = '<a href="#" class="notify" onclick="notify_row(this)">Notify</a>'
  count = 1
  for client in organization['queue']:
    raw += "<tr id='row%s'>" % (count)
    raw += "<td class='client_id'>%s</td>" % (client['client_id'])
    raw += "<td class='telephone'>%s</td>" % (client['phone_number'])
    raw += "<td class='check_in_time'>%s</td>" % (client['check_in'].strftime('%I:%M:%S'))
    if client['notified'] == 'false':
      raw += "<td class='notified_false'>%s</td><td>%s</td>" %  ('No', remove)
    else:
      raw += "<td class='notified_true'>%s</td><td>%s</td>" %  ('Yes', remove)
    raw += "<td>%s</td>" % (notify)
    raw += "<td class='add_type'>%s</td>" % (client['addition_type'])
    raw += "</tr>"
    count += 1
    
  return raw

@view_config(route_name='remove_from_queue', renderer='string')
def remove_queue_entry(request):
  if not all(k in request.POST for k in ('_id', 'client_id')):
    return "NO"
  b_id = request.POST['_id']
  client_id = request.POST['client_id']
  Existing_Client = Client(b_id, None, "manual", client_id)
  if Existing_Client.check_out(request) == False:
    return "NO"
  return "OK"
 
# Adds a user to a queue (manually- this is in the event the user does not have a smartphone)
@view_config(route_name='add_to_queue_manual', renderer='string')
def add_to_queue_manual(request):
  if not all(k in request.POST for k in ('_id', 'client_id', 'tel')):
    return "NO"
  b_id = request.POST['_id']
  client_id = request.POST['client_id']
  telephone =  request.POST['tel']
  New_Client = Client(b_id, telephone, "manual", client_id)
  if New_Client.save(request) == False:
    return "NO"
  return "OK"

# Notifies a user that their spot is ready
@view_config(route_name='notify_user', renderer='string', permission='b_admins')
def notify_user(request):
  if not all(k in request.POST for k in ('_id', 'client_id', 'tel')):
    return "NO"
  b_id = request.POST['_id']
  client_id = request.POST['client_id']
  organization= request.db['organizations'].find_one({'_id' : ObjectId(b_id)})
  for client in organization['queue']:
    if client['client_id'] == client_id:
      client['notified'] = 'true'
      break
  try:
    request.db['organizations'].save(organization)
    return "OK"
  except pymongo.errors.OperationFailure:  
    return "NO"

@view_config(route_name='manage_all', renderer="manage_all.mako", permission='b_queurs')
def manage_all(request):
  if 'u_id' not in request.session:
      return HTTPFound(location=request.route_url('login'))
  u_id = request.session['u_id']
  b_list = []
  user = request.db['users'].find_one({'_id' : ObjectId(u_id)})
  if 'owner' in user:
    for business in user['owner']:
      organization = request.db['organizations'].find_one({'_id' : ObjectId(business)})
      b_list.append({'name' : organization['name'], '_id' : organization['_id'], 'owner':'true'})
  if 'employee' in user:    
    for business in user['employee']:
      flag = True
      organization = request.db['organizations'].find_one({'_id' : ObjectId(business)})
      for item in b_list:
        if item['_id'] == organization['_id']:
          flag = False
      if flag == True:    
        b_list.append({'name' : organization['name'], '_id' : organization['_id'], 'owner':'false'})
  return dict(
    u_id=u_id,
    b_list=b_list,
    logged_in=authenticated_userid(request)
  )
  
@view_config(route_name='manage_employees', renderer="manage_employees.mako", permission='b_admins')
def manage_employees(request):
  if 'u_id' not in request.session:
      return HTTPFound(location=request.route_url('login'))
  u_id = request.session['u_id']
  b_list = []
  user = request.db['users'].find_one({'_id' : ObjectId(u_id)})
  if 'owner' in user:
    for business in user['owner']:
      organization = request.db['organizations'].find_one({'_id' : ObjectId(business)})
      b_list.append({'name' : organization['name'], '_id' : organization['_id']})
  return dict(
    u_id=u_id,
    b_list=b_list,
    logged_in=authenticated_userid(request)
  )

@view_config(route_name='add_employee', renderer='string')
def add_employee(request):
  if not all(k in request.POST for k in ('b_name', 'name', 'p_word')):
    return "NO"
  login = request.POST['name']
  b_id = request.POST['b_name']
  password = request.POST['p_word']
  New_User = User(login, password, ['b_queuers'])
  New_User.employee = [b_id]
  New_User.save(request)
  return "YES"  

@view_config(route_name='check_in', renderer='string')
def check_in(request):
  if not all(k in request.POST for k in ('phone_number', 'restaurant_id')):
    return "NO"
  b_id = request.POST['restaurant_id']
  telephone =  request.POST['phone_number']
  New_Client = Client(b_id, telephone, "manual")
  if New_Client.save(request) == False:
    return "NO"
  return "OK"

@view_config(route_name='check_out', renderer='string')
def check_out(request):
  if not all(k in request.POST for k in ('client_id', 'restaurant_id')):
    return "NO"
  b_id = request.POST['restaurant_id']
  client_id = request.POST['client_id']
  Existing_Client = Client(b_id, None, "manual", client_id)
  if Existing_Client.check_out(request) == False:
    return "NO"
  return "OK"
