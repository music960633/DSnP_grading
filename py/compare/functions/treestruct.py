""" Compare class for "treestruct" method."""

import re

import dsnp_setting
from compare import stat
from compare.functions import base

class TreeStructCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out, regexp='.*'):
    """Compare ref output and student output.

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.
      regexp: Regular expression for filtering.

    Returns:
      Tuple (1, 0, stat.STAT_OK) if the filtered ref_out and stu_out has the
      same tree structure, otherwise return (0, 0, stat.STAT_DIFF).
    """
    ref_match = [s for s in re.findall(regexp, '\n'.join(ref_out)) if s != '']
    stu_match = [s for s in re.findall(regexp, '\n'.join(stu_out)) if s != '']
    ref_tree = self.toTree(ref_match)
    stu_tree = self.toTree(stu_match)
    assert ref_tree is not None, "Parse ref tree error"
    if stu_tree is not None and self.toStr(ref_tree) == self.toStr(stu_tree):
      return (1, 0, stat.STAT_OK)
    else:
      return (0, 0, stat.STAT_DIFF)

  def removeIndent(self, s):
    """Return (num of leading space, string without indent)
      If all characters in s are spaces, return (-1, '').
    """
    spaceArr = map(str.isspace, s)
    if False not in spaceArr:
      return (-1, '')
    index = spaceArr.index(False)
    return (index, s[index:])

  def toTree(self, strList):
    """Transform strList to a tree structure, return None if there is error."""
    arr = filter(lambda x: x[0] != -1, map(self.removeIndent, strList))
    tree = []
    ret = self.toTreeRec(arr, tree)
    return tree if ret else None

  def toTreeRec(self, arr, tree):
    """Recursive build tree, return False if there is error."""
    if len(arr) == 0:
      return True
    indent = arr[0][0]
    # check all indent counts are not larger than indent in first line
    if any(map(lambda x: x[0] < indent, arr)):
      return False
    indexList = [i for i, x in enumerate(arr) if x[0] == indent] + [len(arr)]
    assert indexList[0] == 0
    n = len(indexList)
    for i in range(n - 1):
      subtree = (arr[indexList[i]][1], [])
      ret = self.toTreeRec(arr[indexList[i] + 1 : indexList[i+1]], subtree[1])
      if not ret: return False
      tree.append(subtree)
    return True

  def toStr(self, tree):
    """Transform a tree to string with sorted subtrees"""
    if len(tree) == 0:
      return ''
    return ''.join(sorted(['(' + x[0] + self.toStr(x[1]) + ')' for x in tree]))
