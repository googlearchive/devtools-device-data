#!/usr/bin/env python

import numbers
import os
import os.path
import sys

try:
    import json
except ImportError:
    import simplejson as json

from jsonschema import validate

POSSIBLE_TYPES = ["phone", "tablet", "notebook", "desktop", "unknown"]

def load_and_parse_json(file_name):
  try:
    with open(file_name, "r") as file:
      return json.load(file)
  except:
    print 'ERROR: Failed to parse %s' % file_name
    raise

def raise_type_error(file_name, key, expected_type):
  raise Exception('ERROR: "' + key + '" must be of type "' + expected_type + '" (' + file_name + ')')

def parse_and_rebase_images(images, file_name, prefix, rebase_path):
  for (index, entry) in enumerate(images):
    i = str(index)
    if not isinstance(entry, dict):
      raise_type_error(file_name, prefix + "[" + i + "]", "object")
    if not ("src" in entry) or not isinstance(entry["src"], basestring):
      raise_type_error(file_name, prefix + "[" + i + "]/src", "string")
    if not ("scale" in entry) or not isinstance(entry["scale"], numbers.Number):
      raise_type_error(file_name, prefix + "[" + i + "]/scale", "number")
    entry["src"] = os.path.join(rebase_path, entry["src"])

def parse_orientation(d, file_name, prefix, rebase_path):
  if not ("width" in d) or not isinstance(d["width"], numbers.Number) or d["width"] < 0 or d["width"] > 10000 or abs(d["width"]) != d["width"]:
    raise_type_error(file_name, prefix + "/width", "number")
  if not ("height" in d) or not isinstance(d["height"], numbers.Number) or d["height"] < 0 or d["height"] > 10000 or abs(d["height"]) != d["height"]:
    raise_type_error(file_name, prefix + "/height", "number")

  if not ("outline" in d):
    return
  outline = d["outline"]
  if not isinstance(outline, dict):
    raise_type_error(file_name, prefix + "/outline", "object")
  if not ("images" in outline) or not isinstance(outline["images"], (list, tuple)):
    raise_type_error(file_name, prefix + "/outline/images", "array")
  parse_and_rebase_images(outline["images"], file_name, prefix + "/outline/images", rebase_path)
  if not ("insets" in outline) or not isinstance(outline["insets"], dict):
    raise_type_error(file_name, prefix + "/outline/insets", "object")
  if not ("left" in outline["insets"]) or not isinstance(outline["insets"]["left"], numbers.Number) or outline["insets"]["left"] < 0:
    raise_type_error(file_name, prefix + "/outline/insets/left", "number")
  if not ("top" in outline["insets"]) or not isinstance(outline["insets"]["top"], numbers.Number) or outline["insets"]["top"] < 0:
    raise_type_error(file_name, prefix + "/outline/insets/top", "number")

def parse_modes(modes, file_name, prefix, rebase_path):
  for (index, mode) in enumerate(modes):
    i = str(index)
    if not isinstance(mode, dict):
      raise_type_error(file_name, prefix + "[" + i + "]", "object")
    if not ("title" in mode) or not isinstance(mode["title"], basestring):
      raise_type_error(file_name, prefix + "[" + i + "]/title", "string")
    if not ("orientation" in mode) or not isinstance(mode["orientation"], basestring):
      raise_type_error(file_name, prefix + "[" + i + "]/orientation", "string")
    if mode["orientation"] != "vertical" and mode["orientation"] != "horizontal":
      raise Exception('ERROR: "' + prefix + '[' + i + ']/orientation" must be one of the following: [horizontal, vertical] (' + file_name + ')')

    if not ("images" in mode) or not isinstance(mode["images"], (list, tuple)):
      raise_type_error(file_name, prefix + "[" + i + "]/images", "array")
    parse_and_rebase_images(mode["images"], file_name, prefix + "[" + i + "]/images", rebase_path)

    if not ("page-rect" in mode) or not isinstance(mode["page-rect"], dict):
      raise_type_error(file_name, prefix + "[" + i + "]/page-rect", "object")
    if not ("left" in mode["page-rect"]) or not isinstance(mode["page-rect"]["left"], numbers.Number) or mode["page-rect"]["left"] < 0:
      raise_type_error(file_name, prefix + "[" + i + "]/page-rect/left", "object")
    if not ("top" in mode["page-rect"]) or not isinstance(mode["page-rect"]["top"], numbers.Number) or mode["page-rect"]["top"] < 0:
      raise_type_error(file_name, prefix + "[" + i + "]/page-rect/top", "object")
    if not ("width" in mode["page-rect"]) or not isinstance(mode["page-rect"]["width"], numbers.Number) or mode["page-rect"]["width"] < 0:
      raise_type_error(file_name, prefix + "[" + i + "]/page-rect/width", "object")
    if not ("height" in mode["page-rect"]) or not isinstance(mode["page-rect"]["height"], numbers.Number) or mode["page-rect"]["height"] < 0:
      raise_type_error(file_name, prefix + "[" + i + "]/page-rect/height", "object")

def parse_device_json(file_name, rebase_path):
  json = load_and_parse_json(file_name)
  device_file_schema = load_and_parse_json("device_schema.json")
  validate(json, device_file_schema)

  if not ("title" in json) or not isinstance(json["title"], basestring):
    raise_type_error(file_name, "title", "string")

  if not ("type" in json) or not isinstance(json["type"], basestring):
    raise_type_error(file_name, "type", "string")
  if not (json["type"] in POSSIBLE_TYPES):
    raise Exception('ERROR: "type" must be one of the following: [' + ", ".join(POSSIBLE_TYPES) + '] (' + file_name + ')')

  if not ("user-agent" in json) or not isinstance(json["user-agent"], basestring):
    raise_type_error(file_name, "user-agent", "string")

  if not ("show-by-default" in json) or not isinstance(json["show-by-default"], bool):
    raise_type_error(file_name, "show-by-default", "boolean")

  if not ("capabilities" in json) or not isinstance(json["capabilities"], (list, tuple)):
    raise_type_error(file_name, "capabilities", "array")
  for cap in json["capabilities"]:
    if not isinstance(cap, basestring):
      raise_type_error(file_name, "capability", "string")

  if ("screen" in json) and isinstance(json["screen"], dict):
    screen = json["screen"]
    if not ("device-pixel-ratio" in screen) or not isinstance(screen["device-pixel-ratio"], numbers.Number) or screen["device-pixel-ratio"] < 0 or screen["device-pixel-ratio"] > 100:
      raise_type_error(file_name, "screen/device-pixel-ratio", "number")

    for orientation in ["vertical", "horizontal"]:
      if not (orientation in screen) or not isinstance(screen[orientation], dict):
        raise_type_error(file_name, "screen/" + orientation, "object")
      parse_orientation(screen[orientation], file_name, "screen/" + orientation, rebase_path)
  else:
    raise_type_error(file_name, "screen", "object")

  if "modes" in json:
    if not isinstance(json["modes"], (list, tuple)):
      raise_type_error(file_name, "modes", "array")
    parse_modes(json["modes"], file_name, "modes", rebase_path)

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
