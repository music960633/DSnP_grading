#!/usr/bin/python2.7

import unittest
import tempfile
import os
import shutil

import dsnp_setting
from compare import stat
from compare.functions import filediff

class FileDiffTest(unittest.TestCase):

  def setUp(self):
    self.cls = filediff.FileDiffCmp()
    self.tempdir = tempfile.mkdtemp()
    self.ref_dir = os.path.join(self.tempdir, 'ref_out')
    self.stu_dir = os.path.join(self.tempdir, 'stu_out')
    try:
      os.makedirs(self.ref_dir)
      os.makedirs(self.stu_dir)
    except OSError:
      raise Exception('Cannot create ref_out/ and stu_out/')

  def tearDown(self):
    shutil.rmtree(self.tempdir)

  def testSame(self):
    ref_content = 'aaa\nbbb\n'
    stu_content = 'aaa\nbbb\n'
    filename = 'testsame.out'
    self.writeRefFile(filename, ref_content)
    self.writeStuFile(filename, stu_content)
    kargs = {
      'ref_dir': self.stu_dir,
      'stu_dir': self.ref_dir,
      'filename': filename
    }
    self.assertEqual(self.cls.cmpMisc(**kargs), (1, 0, stat.STAT_OK))

  def testDiff(self):
    ref_content = 'aaa\nbbb\n'
    stu_content = 'aaa\nbbc\n'
    filename = 'testdiff.out'
    self.writeRefFile(filename, ref_content)
    self.writeStuFile(filename, stu_content)
    kargs = {
      'ref_dir': self.stu_dir,
      'stu_dir': self.ref_dir,
      'filename': filename
    }
    self.assertEqual(self.cls.cmpMisc(**kargs), (0, 0, stat.STAT_DIFF))
  
  def writeRefFile(self, filename, content):
    path = os.path.join(self.ref_dir, filename)
    with open(path, 'w') as f:
      f.write(content)

  def writeStuFile(self, filename, content):
    path = os.path.join(self.stu_dir, filename)
    with open(path, 'w') as f:
      f.write(content)


if __name__ == '__main__':
  unittest.main()
