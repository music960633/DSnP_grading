#!/usr/bin/python2.7

import argparse
import os
import sys

import dsnp_setting as dsnp
from utils import parse_util
from utils import shell_util
from utils import task_runner

def setUp(student_list):
  """Create student output directories and copy testdata to them."""
  for student in student_list:
    student_out_dir = os.path.join(dsnp.STU_OUT_DIR, student)
    if not os.path.exists(student_out_dir):
      os.makedirs(student_out_dir)
    shell_util.copyAllFilesToDir(dsnp.DOFILE_DIR, student_out_dir)


def cleanUp(student_list):
  """Delete all testdata in all student output directories."""
  for student in student_list:
    # Delete all testcases
    student_out_dir = os.path.join(dsnp.STU_OUT_DIR, student)
    shell_util.removeDupFilesInDir(dsnp.DOFILE_DIR, student_out_dir)


def runStudent(student_list, case_list, parallel_num):
  """Run all student programs on all cases."""
  task_list = []
  for student in student_list:
    student_dir = os.path.join(dsnp.STU_DIR, student + dsnp.HW_SUFFIX)
    if not os.path.exists(student_dir):
      print 'Directory %s does not exist' % (student + dsnp.HW_SUFFIX)
      continue
    student_exe = os.path.join(student_dir, dsnp.STU_EXE)
    student_out_dir = os.path.join(dsnp.STU_OUT_DIR, student)
    for case in case_list:
      config_file = os.path.join(dsnp.CONFIG_DIR, case + dsnp.JSON_SUFFIX)
      config = parse_util.parseJsonFromFile(config_file)
      assert 'timelimit' in config, 'No timelimit in config'
      assert type(config['timelimit']) == int, "Timelimit shoud be integer"
      # Student out/log is stored in student_out/<student_id>
      student_out = os.path.join(student_out_dir, case + dsnp.OUT_SUFFIX)
      # Add task
      name = '(%s) %s' % (student, case)
      cmd = [student_exe, '-f', case]
      time_limit = config['timelimit']
      mem_limit = config.get('memlimit', 1048576)  # default 1GB
      task = (name, cmd, student_out_dir, student_out, time_limit, mem_limit)
      task_list.append(task)
  runner = task_runner.TaskRunner(task_list, parallel_num)
  runner.run()


def main():
  # Arguments
  parser = argparse.ArgumentParser(description='Run student program.')
  parser.add_argument('case_list_json', type=str,
                      help='Filename for case list in JSON format')
  parser.add_argument('student_list_json', type=str,
                      help='Filename for student list in JSON format')
  parser.add_argument('-p', '--parallel_num', type=int,
                      nargs='?', const=1, default=1,
                      help='Number of parallel tasks, default 1')
  args = parser.parse_args()

  # parallel_num must be greater than 0
  assert args.parallel_num > 0, "parallel_num should be greater than 0."

  # Read case_list and student_list
  case_list = parse_util.parseJsonFromFile(args.case_list_json)
  student_list = parse_util.parseJsonFromFile(args.student_list_json)

  # start running
  setUp(student_list)
  runStudent(student_list, case_list, args.parallel_num)
  cleanUp(student_list)


if __name__ == '__main__':
  main()
