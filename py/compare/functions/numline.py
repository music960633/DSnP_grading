"""Compare class for "numline" compare method."""

import re

import dsnp_setting
from compare import stat
from compare.functions import base

class NumlineCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out, regexp='.*'):
    """Compare ref output and student output.

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.
      regexp: Regular expression for filtering.

    Returns:
      Tuple (1, 0, stat.STAT_OK) if the filtered ref_out and stu_out has the
      same number of lines, otherwise return (0, 0, stat.STAT_DIFF).
    """
    ref_match = [s for s in re.findall(regexp, '\n'.join(ref_out)) if s != '']
    stu_match = [s for s in re.findall(regexp, '\n'.join(stu_out)) if s != '']
    if len(ref_match) == len(stu_match):
      return (1, 0, stat.STAT_OK)
    else:
      return (0, 0, stat.STAT_DIFF)
