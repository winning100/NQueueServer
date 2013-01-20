USERS = {
  'admin':'admin',
  'b_admin':'b_admin',
  'b_worker':'b_worker'
}

GROUPS = {
  'admin':['group:administrator'],
  'b_admin':['group:b_admins', 'group:b_queuer'],
  'b_worker':['group:b_queuer'],
}

COLLECTION = 'users'

def groupfinder(userid, request):
    user = request.db['users'].find_one({"user":userid})
    if user:
      return [('group:%s' % role) for role in user['groups']]
    else:
      return None

