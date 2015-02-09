#!/usr/bin/env python

import os
import os.path
import sys

try:
    import json
except ImportError:
    import simplejson as json

from jsonschema import validate

def load_and_parse_json(file_name):
  try:
    with open(file_name, "r") as file:
      return json.load(file)
  except:
    print 'ERROR: Failed to parse %s' % file_name
    raise

def raise_type_error(file_name, key, expected_type):
  raise Exception('ERROR: "' + key + '" must be of type "' + expected_type + '" (' + file_name + ')')

def parse_and_rebase_images(images, rebase_path):
  for (index, entry) in enumerate(images):
    entry["src"] = os.path.join(rebase_path, entry["src"])

def parse_orientation(d, file_name, prefix):
  if abs(d["width"]) != d["width"]:
    raise_type_error(file_name, prefix + "/width", "number")

  if abs(d["height"]) != d["height"]:
    raise_type_error(file_name, prefix + "/height", "number")

  if not ("outline" in d):
    return

  outline = d["outline"]

  parse_and_rebase_images(outline["images"], file_name)

def parse_modes(modes, file_name):
  for (index, mode) in enumerate(modes):
    parse_and_rebase_images(mode["images"], file_name)

def parse_device_json(file_name, rebase_path):
  json = load_and_parse_json(file_name)
  device_file_schema = load_and_parse_json("device_schema.json")
  validate(json, device_file_schema)

  screen = json["screen"]

  for orientation in ["vertical", "horizontal"]:
    parse_orientation(screen[orientation], file_name, "screen/" + orientation)

  if "modes" in json:
    parse_modes(json["modes"], file_name)

  return json

def main(argv):
  root_path = os.path.dirname(os.path.abspath(__file__))
  all_files = os.listdir(root_path)
  devices_json = []
  for file_name in all_files:
    dir_name = os.path.join(root_path, file_name)
    device_file_name = os.path.join(dir_name, "device.json")
    if os.path.isdir(dir_name) and os.path.isfile(device_file_name):
      devices_json.append(parse_device_json(device_file_name, file_name))

  result_json = {}
  result_json["version"] = 1
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
