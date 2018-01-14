#!/usr/bin/python2.7

import unittest

import dsnp_setting
from compare import stat
from compare.functions import treestruct

class TreeStructTest(unittest.TestCase):

  def setUp(self):
    self.cls = treestruct.TreeStructCmp()

  def testRemoveIndent(self):
    self.assertEqual(self.cls.removeIndent('  abc'), (2, 'abc'))
    self.assertEqual(self.cls.removeIndent('   '), (-1, ''))

  def testToTree(self):
    # Simple case
    arr = ['  root']
    self.assertEqual(self.cls.toTree(arr), [('root', [])])
    # Complex case
    arr = ['root', '  child_1', '   child_1_1', '  child_2', 'root 2']
    expected = [('root', [
                  ('child_1', [
                    ('child_1_1', [])]),
                  ('child_2', [])]),
                ('root 2', [])]
    self.assertEqual(self.cls.toTree(arr), expected)

  def testToTreeError(self):
    # Children should have same indent
    arr = ['root', '  child1', ' child2']
    self.assertEqual(self.cls.toTree(arr), None)
    # Even for root
    arr = [' root1', 'root2']
    self.assertEqual(self.cls.toTree(arr), None)

  def testToString(self):
    tree = [('b', [('d', []), ('c', []), ('e', [])]), ('a', [])]
    expected = '(a)(b(c)(d)(e))'
    self.assertEqual(self.cls.toStr(tree), expected)

  def testCmp(self):
    ref_out = ['AIG 1',
               '  AIG 2',
               '  !AIG 3',
               '    AIG 5',
               '    AIG 4'
              ]
    stu_out = ['AIG 1',
               '  !AIG 3',
               '    AIG 4',
               '    AIG 5',
               '         ',  # an empty line does not matter
               '  AIG 2'
              ]
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (1, 0, stat.STAT_OK))
    ref_out = ['AIG 1',
               '  AIG 2',
               '  !AIG 3',
               '    AIG 5',
               '    AIG 4'
              ]
    stu_out = ['AIG 1',
               '  !AIG 3',
               '  AIG 2',
               '    AIG 5',
               '    AIG 4'
              ]
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out), (0, 0, stat.STAT_DIFF))

  def testRegexp(self):
    regexp = ' *!?AIG| *!?PI'
    ref_out = ['AIG 1',
               '  AIG 2',
               '  !AIG 3',
               '    AIG 5',
               '    PI 4'
              ]
    stu_out = ['AIG 10',
               '  !AIG 30',
               '    AIG 50',
               '    PI 40',
               '  AIG 20',
               '  meow'  # MEOW~
              ]
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, regexp=regexp),
                     (1, 0, stat.STAT_OK))
    ref_out = ['AIG 1',
               '  AIG 2',
               '  !AIG 3',
               '    AIG 5',
               '    PI 4'
              ]
    stu_out = ['AIG 10',
               '  AIG 30',
               '    AIG 50',
               '    PI 40',
               '  !AIG 20',
              ]
    self.assertEqual(self.cls.cmpCmd(ref_out, stu_out, regexp=regexp),
                     (0, 0, stat.STAT_DIFF))
    

if __name__ == '__main__':
  unittest.main()
