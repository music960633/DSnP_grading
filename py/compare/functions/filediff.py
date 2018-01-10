"""Compare class for "filediff" compare method."""

import os

import dsnp_setting as dsnp
from compare import stat
from compare.functions import base

class FileDiffCmp(base.BaseCmp):
  def cmpMisc(self, ref_dir, stu_dir, filename):
    """Compare ref output file and student output file.

    Args:
      student: Student ID.
      filename: File to compare.

    Returns:
      Tuple (1, 0, stat.STAT_NOFILE) if student output file is not found. If
      the output files match, return (1, 0, stat.STAT_OK), otherwise return
      (0, 0, stat.STAT_DIFF).
    """
    ref_file = os.path.join(ref_dir, filename)
    stu_file = os.path.join(stu_dir, filename)
    assert os.path.exists(ref_file), 'Ref file %s does not exist!' % ref_file
    if not os.path.exists(stu_file):
      return (0, stat.STAT_NOFILE)
    ret = os.system('diff -q %s %s >/dev/null' % (ref_file, stu_file))
    if ret == 0:
      return (1, 0, stat.STAT_OK)
    else:
      return (0, 0, stat.STAT_DIFF)
