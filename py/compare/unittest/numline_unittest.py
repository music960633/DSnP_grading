#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import numline

class NumlineTest(unittest.TestCase):

  def setUp(self):
    self.cls = numline.NumlineCmp()

  def testSame(self):
    ref_out = ['a', 'b']
    stu_out = ['c', 'd']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))

  def testDiff(self):
    ref_out = ['a', 'b']
    stu_out = ['c', 'd', 'e']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (0, 0, stat.STAT_DIFF))

  def testRegexp(self):
    ref_out = ['[1] a', '[2] b']
    stu_out = ['[1] c', '[2] d', 'e']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, regexp='\[\d+\].*'),
                     (1, 0, stat.STAT_OK))
    ref_out = ['[1] a', '[2] b']
    stu_out = ['[1] c', '[2] d', '[3] e']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, regexp='\[\d+\].*'),
                     (0, 0, stat.STAT_DIFF))


if __name__ == '__main__':
  unittest.main()
