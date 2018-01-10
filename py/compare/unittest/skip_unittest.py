#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import skip

class SkipTest(unittest.TestCase):

  def setUp(self):
    self.cls = skip.SkipCmp()

  def testSame(self):
    ref_out = ['a', 'b']
    stu_out = ['a', 'b']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))

  def testDiff(self):
    ref_out = ['a', 'b']
    stu_out = ['a', 'c']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))
  

if __name__ == '__main__':
  unittest.main()
