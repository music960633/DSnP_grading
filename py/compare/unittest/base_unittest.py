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

  def testUpdateScore(self):
    self.assertEqual(self.cls.updateScore(10, 100, 0.5), 60)

  def testUpdatePenalty(self):
    self.assertEqual(self.cls.updatePenalty(0, 0.5), 0.5)
    self.assertEqual(self.cls.updatePenalty(0.5, 2), 1)

  def testUpdateStatus(self):
    self.assertEqual(self.cls.updateStatus(stat.STAT_OK, stat.STAT_OK),
                     stat.STAT_OK)
    self.assertEqual(self.cls.updateStatus(stat.STAT_OK, stat.STAT_DIFF),
                     stat.STAT_DIFF)
    self.assertEqual(self.cls.updateStatus(stat.STAT_DIFF, stat.STAT_OK),
                     stat.STAT_DIFF)
    self.assertEqual(self.cls.updateStatus(stat.STAT_ERROR, stat.STAT_DIFF),
                     stat.STAT_ERROR)

  def testInheritClass(self):
    class TestCmp(base.BaseCmp):
      def cmpCmd(self, ref_out, stu_out):
        return (1, 0, stat.STAT_DIFF)
      def cmpMisc(self):
        return (0.5, 2, stat.STAT_PENALTY)

    testCmp = TestCmp()
    self.assertEqual(testCmp.evalCmd(1, 0.5, stat.STAT_OK, 10, [], []),
                     (11, 0.5, stat.STAT_DIFF))
    self.assertEqual(testCmp.evalMisc(1, 0, stat.STAT_OK, 10),
                     (6, 1, stat.STAT_PENALTY))


if __name__ == '__main__':
  unittest.main()
