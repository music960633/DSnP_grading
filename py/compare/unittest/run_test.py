#!/usr/bin/python2.7

"""Run all unittests in py/compare/functions directory."""

import os
import argparse

import dsnp_setting as dsnp
from utils import task_runner

def runUnittest(parallel_num):
  functions_path = os.path.join(dsnp.ROOT, 'py', 'compare', 'unittest')
  task_list = [(test, './' + test, functions_path, '/dev/null', 1, 32 * 1024)
               for test in os.listdir(functions_path)
               if test.endswith('_unittest.py')]
  runner = task_runner.TaskRunner(task_list, parallel_num)
  runner.run()


def main():
  # Arguments
  parser = argparse.ArgumentParser(description='Run unittests.')
  parser.add_argument('-p', '--parallel_num', type=int,
                      nargs='?', const=1, default=1,
                      help='Number of parallel tasks, default 1')
  args = parser.parse_args()

  # parallel_num must be greater than 0
  assert args.parallel_num > 0, "parallel_num should be greater than 0."

  # Start running
  runUnittest(args.parallel_num)


if __name__ == '__main__':
  main()
