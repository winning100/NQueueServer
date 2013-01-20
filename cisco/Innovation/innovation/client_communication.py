from pymongo.errors import InvalidId
from bson.objectid import ObjectId
import json
import urllib2


url = 'https://android.googleapis.com/gcm/send'
key = 'AIzaSyDQ4vNuBmnDqk_QmkIs_g9zbs_3gB2'


def send_notification(request, _id, message):
  json_data = {
    'registration_ids' : [_id],
    'data' : {
      'message' : message,
    }
  }
  data_to_send = json.dumps(json_data)
  key_to_send = "key=" + key
  headers = {'Content-Type': 'application/json', 'Authorization': key}
  request = urllib2.Request(url, data_to_send, headers)
  handler = urllib2.urlopen(request)
  response = json.loads(handler.read())
  reply = {}
  if response ['failure'] == 0:
    reply['error'] = '0'
  else:
    response ['error'] = '1'
  return HttpResponse(json.dumps(reply), mimetype="application/javascript")

