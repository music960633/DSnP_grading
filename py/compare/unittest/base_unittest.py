#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import base

class BaseTest(unittest.TestCase):

  def setUp(self):
    self.cls = base.BaseCmp()

  def testException(self):
    ref_out = ['a', 'b']
    stu_out = ['a', 'b']
    self.assertRaises(NotImplementedError, self.cls.cmpCmd, ref_out, stu_out)
    self.assertRaises(NotImplementedError, self.cls.cmpMisc)

  def testInheritClass(self):
    class TestCmp(base.BaseCmp):
      def cmpCmd(self, ref_out, stu_out):
        return (1, 0, stat.STAT_DIFF)
      def cmpMisc(self):
        return (0.5, 2, stat.STAT_OK)

    testCmp = TestCmp()
    self.assertEqual(testCmp.evalCmd(10, [], []), (10, 0, stat.STAT_DIFF))
    self.assertEqual(testCmp.evalMisc(10), (5, 2, stat.STAT_OK))


if __name__ == '__main__':
  unittest.main()
