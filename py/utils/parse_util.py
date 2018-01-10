import os
import json

def parseJsonFromFile(filename):
  if not os.path.exists(filename):
    raise Exception('File \"%s\" does not exist.' % filename)
  try:
    with open(filename, 'r') as f:
      res = json.load(f)
  except ValueError, err:
    raise Exception('File \"%s\" has invalid JSON format' % filename)
  return res
