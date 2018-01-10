"""Compare class for "skip" compare method."""

import dsnp_setting
from compare import stat
from compare.functions import base

class SkipCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out):
    """Compare ref output and student output.

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.

    Returns:
      Always return (1, 0, stat.STAT_OK).
    """
    return (1, 0, stat.STAT_OK)
