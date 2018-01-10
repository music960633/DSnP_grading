#!/usr/bin/python2.7

"""A simple script to generate a default JSON config for a dofile.

Usage: ./dofile_to_config.py <dofile> <config>

The default scoring method is "skip", which actually does nothing.
"""

import sys
import json
import collections

def main():
  if len(sys.argv) != 3:
    print "Usage: %s <dofile> <config>" % sys.argv[0]

  dofile_name = sys.argv[1]
  config_name = sys.argv[2]
  config = collections.OrderedDict([('prompt', 'fraig>'), ('timelimit', 1)])
  evalList = []
  with open(sys.argv[1], "r") as f:
    for s in f:
      s = s.strip()
      evalItem = collections.OrderedDict(
          [('type', 'cmd'), ('__cmd', s), ('score', 0), ('method', 'skip')])
      evalList.append(evalItem)
  config['evalList'] = evalList
  with open(config_name, "w") as f:
    json.dump(config, f, indent = 2, separators = (',', ': '))

if __name__ == '__main__':
  main()
