#!/usr/bin/python2.7

import argparse
import os
import sys

import dsnp_setting as dsnp
from utils import parse_util
from utils import shell_util
from utils import task_runner

def setUp():
  """Create ref output directory and copy testdata to it."""
  if not os.path.exists(dsnp.REF_OUT_DIR):
    os.makedirs(dsnp.REF_OUT_DIR)
  shell_util.copyAllFilesToDir(dsnp.DOFILE_DIR, dsnp.REF_OUT_DIR)


def cleanUp():
  """Delete all testdata in ref output directory."""
  shell_util.removeDupFilesInDir(dsnp.DOFILE_DIR, dsnp.REF_OUT_DIR)


def runRef(case_list, parallel_num):
  """Run ref program on all cases."""
  task_list = []
  ref_exe = os.path.join(dsnp.REF_DIR, dsnp.REF_EXE)
  for case in case_list:
    config_file = os.path.join(dsnp.CONFIG_DIR, case + dsnp.JSON_SUFFIX)
    config = parse_util.parseJsonFromFile(config_file)
    assert 'timelimit' in config, 'No timelimit in config'
    assert type(config['timelimit']) == int, "Timelimit shoud be integer"
    # Ref out/log is stored in REF_OUT_DIR
    ref_out = os.path.join(dsnp.REF_OUT_DIR, case + dsnp.OUT_SUFFIX)
    # Add task
    name = '(Ref) ' + case
    cmd = [ref_exe, '-f', case]
    time_limit = config['timelimit']
    mem_limit = config.get('memlimit', 1048576)  # default 1GB
    task = (name, cmd, dsnp.REF_OUT_DIR, ref_out, time_limit, mem_limit)
    task_list.append(task)
  runner = task_runner.TaskRunner(task_list, parallel_num)
  runner.run()


def main():
  # Arguments
  parser = argparse.ArgumentParser(description='Run reference program.')
  parser.add_argument('case_list_json', type=str,
                      help='Filename for case list in JSON format')
  parser.add_argument('-p', '--parallel_num', type=int,
                      nargs='?', const=1, default=1,
                      help='Number of parallel tasks, default 1')
  args = parser.parse_args()

  # parallel_num must be greater than 0
  assert args.parallel_num > 0, "parallel_num should be greater than 0."

  # Read case_list
  case_list = parse_util.parseJsonFromFile(args.case_list_json)

  # Start running
  setUp()
  runRef(case_list, args.parallel_num)
  cleanUp()


if __name__ == '__main__':
  main()
