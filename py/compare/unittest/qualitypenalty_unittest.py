#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import qualitypenalty

class QualityPenaltyTest(unittest.TestCase):

  def setUp(self):
    self.cls = qualitypenalty.QualityPenaltyCmp()

  def testQuality(self):
    ref_out = ['Total 100']
    stu_out_better = ['Total  90']
    stu_out_same = ['Total  100']
    stu_out_med = ['Total 125']
    stu_out_bad = ['Total 221']
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_better, y=10),
                     (0, 0, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_same, y=10),
                     (0, 0, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_med, y=10),
                     (0, 0.5, stat.STAT_PENALTY))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_bad, y=10),
                     (0, 1.1, stat.STAT_PENALTY))

  def testException(self):
    ref_out = ['Total meow']
    stu_out = ['Total 100']
    self.assertRaises(AssertionError, self.cls.cmpCmd, ref_out, stu_out)
  

if __name__ == '__main__':
  unittest.main()
