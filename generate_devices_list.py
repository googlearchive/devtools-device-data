#!/usr/bin/env python

import os
import os.path
import sys

try:
    import json
except ImportError:
    import simplejson as json

def load_and_parse_json(file_name):
  try:
    with open(file_name, "r") as file:
      return json.load(file)
  except:
    print 'ERROR: Failed to parse %s' % file_name
    raise

def rebase_images(json, rebase_path):
  for entry in json:
    if entry["file"]:
      entry["file"] = os.path.join(rebase_path, entry["file"])

def read_device_json(file_name, rebase_path):
  json = load_and_parse_json(file_name)
  if json["outline"] and json["outline"]["images"]:
    rebase_images(json["outline"]["images"], rebase_path)

  if json["modes"]:
    for mode_json in json["modes"]:
      if mode_json["images"]:
        rebase_images(mode_json["images"], rebase_path)

  return json

def main(argv):
  root_path = os.path.dirname(os.path.abspath(__file__))
  all_files = os.listdir(root_path)
  devices_json = []
  for file_name in all_files:
    dir_name = os.path.join(root_path, file_name)
    device_file_name = os.path.join(dir_name, "device.json")
    if os.path.isdir(dir_name) and os.path.isfile(device_file_name):
      devices_json.append(read_device_json(device_file_name, file_name))

  result_json = {}
  result_json["version"] = "1.0"
  result_json["devices"] = devices_json

  list_file_name = os.path.join(root_path, "devices.json")
  try:
    with open(list_file_name, "w") as file:
      json.dump(result_json, file)
  except:
    print 'ERROR: Failed to write %s' % list_file_name
    raise

if __name__ == '__main__':
  sys.exit(main(sys.argv))
