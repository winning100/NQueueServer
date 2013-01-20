from pyramid.security import Everyone
from pyramid.security import Authenticated
from pyramid.security import ( 
  Allow,
  Everyone,
  ALL_PERMISSIONS,
  )
import bcrypt
import uuid
import datetime
from pymongo.errors import InvalidId
from bson.objectid import ObjectId

class User(object):
  def __init__(self, login, password, groups=None):
    self.login = login
    self.password = password
    self.groups = groups or [] 
    self.owner = []
    self.employee = []
    self._id = None

  def authenticate(self, request):
    user = request.db['users'].find_one({"user":self.login})
    if user:
      if bcrypt.hashpw(self.password, user['salt']) == user['password']:
        self.groups = user['groups']
        self._id = user['_id']
        return True
    return False

  def _role_filter(self, request):
    user = request.db['users'].find_one({"user":self.login})
    if user:
      return [('group:%s' % role.name) for role in user['groups']]
  
  def _set_password(self, request, password):
    salt = bcrypt.gensalt()
    new_password = bcrypt.hashpw(password, salt)
    request.db['users'].update( { '_id' : self._id }, { 'password' : bcrypt.hashpw(self.password, salt), 'salt' : salt } ) 

  def _add_groups(self, request, owner, employee):
    self.owner = owner
    self.employee = employee

  def save(self, request):
    salt = bcrypt.gensalt()
    save_dict = {
      'groups':self.groups, 
      'owner' : self.owner, 
      'employee' : self.employee, 
      'user' : self.login,
      'password' : bcrypt.hashpw(self.password, salt),
      'salt' : salt
    }
    try:
      request.db['users'].save(save_dict)
      return True
    except pymongo.errors.OperationFailure:  
      return False

class Client(object):
  def __init__(self, r_id, telephone, check_in_type, client_id=None):
    self.r_id = r_id
    self.telephone = telephone
    self.client_id = client_id or uuid.uuid1()
    self.check_in_type = check_in_type
  
  def save(self, request):
    add_dict = {
      'client_id' : self.client_id,
      'phone_number' : self.telephone, 
      'check_in' : datetime.datetime.now(), 
      'notified' : 'false', 
      'addition_type' : self.check_in_type
    }
    organization= request.db['organizations'].find_one({'_id' : ObjectId(self.r_id)})
    organization['queue'].append(add_dict)
    try:
      request.db['organizations'].save(organization)
      return True
    except pymongo.errors.OperationFailure:  
      return False

  def check_out(self, request):
    organization= request.db['organizations'].find_one({'_id' : ObjectId(self.r_id)})
    organization['queue'][:] = [d for d in organization['queue'] if d.get('client_id') != self.client_id]     
    try:
      request.db['organizations'].save(organization)
      return True
    except pymongo.errors.OperationFailure:  
      return False

# Unused
class Organization(object):
  def __init__(self, name):
    self.name = name
    self.queue = []

  def locate(self, request, b_id):
    request.db['organizations'].find_one({'_id' : ObjectId(b_id) })

class RootFactory(object):
    __acl__ = [
        (Allow, Everyone, 'view'),
        (Allow, 'group:b_admins', ALL_PERMISSIONS),
        (Allow, 'group:b_queuer', 'b_queuers')
    ]  

    def __init__(self, request):
        pass  # pragma: no cover
