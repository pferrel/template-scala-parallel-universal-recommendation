"""
Import sample data for recommendation engine
"""

import predictionio
import argparse
import random
import datetime
import pytz

RATE_ACTIONS_DELIMITER = ","
PROPERTIES_DELIMITER = ":"
SEED = 1


def import_events(client, file):
  f = open(file, 'r')
  random.seed(SEED)
  count = 0
  # year, month, day[, hour[, minute[, second[
  #event_date = datetime.datetime(2015, 8, 13, 12, 24, 41)
  now_date = datetime.datetime.now(pytz.utc) # - datetime.timedelta(days=2.7)
  current_date = now_date
  event_time_increment = datetime.timedelta(days= -0.8)
  available_date_increment = datetime.timedelta(days= 0.8)
  event_date = now_date - datetime.timedelta(days= 2.4)
  available_date = event_date + datetime.timedelta(days=-2)
  expire_date = event_date + datetime.timedelta(days=2)
  print "Importing data..."

  for line in f:
    data = line.rstrip('\r\n').split(RATE_ACTIONS_DELIMITER)
    # For demonstration purpose action names are taken from input along with secondary actions on
    # For the UR add some item metadata

    if (data[1] == "purchase"):
      client.create_event(
        event=data[1],
        entity_type="user",
        entity_id=data[0],
        target_entity_type="item",
        target_entity_id=data[2],
        event_time = current_date
      )
      print "Event: " + data[1] + " entity_id: " + data[0] + " target_entity_id: " + data[2] + \
            " current_date: " + current_date.isoformat()
    elif (data[1] == "view"):  # assumes other event type is 'view'
      client.create_event(
        event=data[1],
        entity_type="user",
        entity_id=data[0],
        target_entity_type="item",  # type of item in this action
        target_entity_id=data[2],
        event_time = current_date
      )
      print "Event: " + data[1] + " entity_id: " + data[0] + " target_entity_id: " + data[2] + \
            " current_date: " + current_date.isoformat()
    elif (data[1] == "$set"):  # must be a set event
      properties = data[2].split(PROPERTIES_DELIMITER)
      prop_name = properties.pop(0)
      prop_value = properties if not prop_name == 'defaultRank' else float(properties[0])
      client.create_event(
        event=data[1],
        entity_type="item",
        entity_id=data[0],
        event_time=current_date,
        properties={prop_name: prop_value}
      )
      print "Event: " + data[1] + " entity_id: " + data[0] + " properties/"+prop_name+": " + str(properties) + \
          " current_date: " + current_date.isoformat()
    count += 1
    current_date += event_time_increment

  items = ['Iphone 6', 'Ipad-retina', 'Nexus', 'Surface', 'Iphone 4', 'Galaxy', 'Iphone 5']
  print "All items: " + str(items)
  for item in items:

    client.create_event(
      event="$set",
      entity_type="item",
      entity_id=item,
      properties={"expires": expire_date.isoformat(),
                  "available": available_date.isoformat(),
                  "date": event_date.isoformat()}
    )
    print "Event: $set entity_id: " + item + \
            " properties/availableDate: " + available_date.isoformat() + \
            " properties/date: " + event_date.isoformat() + \
            " properties/expireDate: " + expire_date.isoformat()
    expire_date += available_date_increment
    event_date += available_date_increment
    available_date += available_date_increment
    count += 1

  f.close()
  print "%s events are imported." % count


# very simple dictionary to json string conversion
def dict_to_jsonstr(d):
  jsonstr = '{'
  valcount = 0
  for key_name in d:
    if valcount > 0:
      jsonstr += ', '
    valcount += 1
    jsonstr += '"' + snake_to_camel_case(key_name) + '":' + val_to_jsonstr(d[key_name])
  jsonstr += '}'
  return jsonstr

# convert a x_yz string to xYz
def snake_to_camel_case(key_name):
  java_name = ""
  saw_underscore = False
  for c in key_name:
    if c == '_':
      saw_underscore = True
    else:
      if saw_underscore:
        java_name += c.upper()
        saw_underscore = False
      else:
        java_name += c
  return java_name

def list_to_jsonstr(l):
  jsonstr = '['
  valcount = 0
  for val in l:
    if valcount > 0:
      jsonstr += ', '
    valcount += 1
    jsonstr += val_to_jsonstr(val)
  jsonstr += ']'
  return jsonstr

def val_to_jsonstr(v):
  jsonstr = ""
  if type(v) is str:
    jsonstr += '"' + v + '"'
  elif type(v) is dict:
    jsonstr += dict_to_jsonstr(v)
  elif type(v) is list:
    jsonstr += list_to_jsonstr(v)
  else:
    jsonstr += v
  return jsonstr


# provide an alternate client for the --json_out option
class JsonClient:
  def __init__(self, filename):
    self.fp = open(filename, 'w')

  def create_event(self, **kwargs):
    jsonstr = dict_to_jsonstr(kwargs)
    self.fp.write(jsonstr)
    self.fp.write('\n')


if __name__ == '__main__':
  parser = argparse.ArgumentParser(
    description="Import sample data for recommendation engine")
  parser.add_argument('--access_key', default='invald_access_key')
  parser.add_argument('--url', default="http://localhost:7070")
  parser.add_argument('--file', default="./data/sample-handmade-data.txt")
  parser.add_argument('--json_out', default="my_events.json", help='write JSON-formatted events to this file instead')

  args = parser.parse_args()
  print args

  if args.json_out is None:
    client = predictionio.EventClient(
      access_key=args.access_key,
      url=args.url,
      threads=5,
      qsize=500)
  else:
    client = JsonClient(args.json_out)

  import_events(client, args.file)
