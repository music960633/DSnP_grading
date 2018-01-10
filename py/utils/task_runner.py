import os
import sys
import termios
import signal
import subprocess
import threading
import time

import dsnp_setting
from utils import shell_util

class Task(object):
  def __init__(self, cmd, cwd, out_filename, time_limit, mem_limit):
    self.cmd = cmd
    self.start_time = time.time()
    self.time_limit = time_limit
    self.mem_limit = mem_limit
    self.out = open(out_filename, 'w')
    self.err = open(os.devnull, 'r+')
    self.proc = subprocess.Popen(cmd, stdout = self.out, stderr = self.err,
                                 cwd = cwd)
    self.retcode = None
    
    watch_thread = threading.Thread(target = self.watch)
    watch_thread.daemon = True
    watch_thread.start()

  def watch(self):
    while True:
      time.sleep(0.1)
      if self.retcode is not None:
        break
      if time.time() > self.start_time + self.time_limit:
        os.kill(self.proc.pid, signal.SIGINT)
        self.out.flush()
        self.out.write('\nTIMEOUT')
        break
      if shell_util.getMemUsage(self.proc.pid) > self.mem_limit:
        os.kill(self.proc.pid, signal.SIGINT)
        self.out.flush()
        self.out.write('\nMEMOUT')
        break
    self.out.close()
    self.err.close()


class TaskRunner(object):
  def __init__(self, task_list, parallel_num):
    self.task_list = task_list
    self.parallel_num = parallel_num
    self.running_task = {}
    self.event = threading.Event()
    self.tot = len(task_list)
    self.done = 0
    self.orig_tty = termios.tcgetattr(sys.stdin)

    # event handler
    def handler(sig, frame):
      self.event.set()
      print 'Terminate all tasks'
    signal.signal(signal.SIGINT, handler)

  def run(self):
    self.checkMemory()
    self.done = 0
    for name, cmd, cwd, out_filename, time_limit, mem_limit in self.task_list:
      task = Task(cmd, cwd, out_filename, time_limit, mem_limit)
      self.running_task[task.proc.pid] = (name, task)
      self.waitUntilLessThan(self.parallel_num)
    self.waitUntilLessThan(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_tty)

  def waitUntilLessThan(self, num):
    while len(self.running_task) >= num:
      if self.event.isSet():
        self.killAllTask()
      pid, status = os.waitpid(-1, os.WNOHANG)
      if pid != 0:
        name, task = self.running_task.pop(pid)
        self.done += 1
        message = '[%d/%d] %s' % (self.done, self.tot, name)
        if os.WIFEXITED(status):
          task.retcode = os.WEXITSTATUS(status)
        else:
          task.retcode = -1
        if task.retcode == 0:
          self.messageNormal(message)
        else:
          self.messageError(message)
      else:
        self.event.wait(0.1)

  def killAllTask(self):
    for pid in self.running_task:
      os.kill(pid, signal.SIGINT)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.orig_tty)
    raise KeyboardInterrupt()

  def messageNormal(self, message):
    print '\033[22;32m%s\033[22;0m' % message

  def messageError(self, message):
    print '\033[22;31m%s\033[22;0m' % message

  def checkMemory(self):
    if not shell_util.checkMemProbe():
      print '[Warning] Memory usage cannot be probed.'
