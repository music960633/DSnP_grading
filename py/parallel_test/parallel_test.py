#!/usr/bin/python2.7

import os
import shutil
import tempfile

import dsnp_setting
from utils import task_runner

def runParallel(parallel_num):
  # create temp dir
  tempdir = tempfile.mkdtemp()
  # setup tasks and run
  task_list = []
  for i in range(parallel_num):
    name = 'parallel_%d_%d' % (i + 1, parallel_num)
    cmd = './bubble_sort.py'
    cwd = './'
    out = os.path.join(tempdir, name + '.out')
    time_limit = 100
    mem_limit = 1048576  # 1GB
    task = (name, cmd, cwd, out, time_limit, mem_limit)
    task_list.append(task)
  runner = task_runner.TaskRunner(task_list, parallel_num, show_progress=False)
  runner.run()
  # calculate average time
  tot_runtime = 0.0
  for i in range(parallel_num):
    name = 'parallel_%d_%d.out' % (i + 1, parallel_num)
    path = os.path.join(tempdir, name)
    with open(path, 'r') as f:
      runtime = float(f.read())
    tot_runtime += runtime
  # remove temp dir
  shutil.rmtree(tempdir)
  # return average
  return tot_runtime / parallel_num


def main():
  for i in range(1, 20):
    runtime = runParallel(i)
    if i == 1:
      basetime = runtime
    print '%d cores: %f' % (i, runtime)
    if runtime > 2 * basetime:
      print 'Too slow!!'
      break


if __name__ == '__main__':
  main()
