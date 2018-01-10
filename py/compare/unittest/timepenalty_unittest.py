#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import timepenalty

class TimePenaltyTest(unittest.TestCase):

  def setUp(self):
    self.cls = timepenalty.TimePenaltyCmp()

  def testAbsolute(self):
    ref_out = ['Total time used : 10 seconds']
    stu_out_fast = ['Total time used: 19 seconds']
    stu_out_med1 = ['Total time used: 25 seconds']
    stu_out_med2 = ['Total time used: 40.00 seconds']
    stu_out_slow = ['Total time used: 50.22 seconds']
    kargs = {
      'min_val': 20,
      'max_val': 50,
      'min_penalty': -0.5,
      'max_penalty': 1.0
    }
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_fast, **kargs),
                     (0, -0.5, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_med1, **kargs),
                     (0, -0.25, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_med2, **kargs),
                     (0, 0.5, stat.STAT_PENALTY))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_slow, **kargs),
                     (0, 1.0, stat.STAT_PENALTY))
  
  def testRelative(self):
    ref_out = ['Total time used : 10 seconds']
    stu_out_fast = ['Total time used: 19 seconds']
    stu_out_med1 = ['Total time used: 25 seconds']
    stu_out_med2 = ['Total time used: 40.00 seconds']
    stu_out_slow = ['Total time used: 50.22 seconds']
    kargs = {
      'min_val': 2.0,
      'max_val': 5.0,
      'min_penalty': -0.5,
      'max_penalty': 1.0,
      "relative": True
    }
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_fast, **kargs),
                     (0, -0.5, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_med1, **kargs),
                     (0, -0.25, stat.STAT_OK))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_med2, **kargs),
                     (0, 0.5, stat.STAT_PENALTY))
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out_slow, **kargs),
                     (0, 1.0, stat.STAT_PENALTY))


if __name__ == '__main__':
  unittest.main()
