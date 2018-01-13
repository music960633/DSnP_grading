#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import diff

class DiffTest(unittest.TestCase):

  def setUp(self):
    self.cls = diff.DiffCmp()

  def testSame(self):
    ref_out = ['a', 'b']
    stu_out = ['a', 'b']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))

  def testDiff(self):
    ref_out = ['a', 'b']
    stu_out = ['a', 'c']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (0, 0, stat.STAT_DIFF))

  def testRegexp(self):
    ref_out = ['meow', 'meoww!', 'mmeow']
    stu_out = ['meow', 'meoww', 'meow', 'meeeow']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (0, 0, stat.STAT_DIFF))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, regexp='meow*'),
                     (1, 0, stat.STAT_OK))

  def testSort(self):
    ref_out = ['a', 'b']
    stu_out = ['b', 'a']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (0, 0, stat.STAT_DIFF))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, sort=True),
                     (1, 0, stat.STAT_OK))

  def testStrict(self):
    ref_out = ['a b']
    stu_out = ['a  b']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, strict=True),
                     (0, 0, stat.STAT_DIFF))

  def testExtraSpace(self):
    self.assertEqual(self.cls.cmpCmd(['ab'], ['a b']), (0, 0, stat.STAT_DIFF))
    self.assertEqual(self.cls.cmpCmd(['a b'], ['ab']), (0, 0, stat.STAT_DIFF))

  

if __name__ == '__main__':
  unittest.main()
