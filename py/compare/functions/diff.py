"""Compare class for "diff" compare method."""

import re

import dsnp_setting
from compare import stat
from compare.functions import base

class DiffCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out, regexp='.*', sort=False, strict=False):
    """Compare ref output and student output.

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.
      regexp: Regular expression for filtering.
      sort: Sort the outputs or not
      strict: Use strict compare, do not remove extra white spaces.

    Returns:
      Tuple (1, 0, stat.STAT_OK) if the filtered ref_out and stu_out match,
      otherwise return (0, 0, stat.STAT_DIFF).
    """
    ref_match = [s for s in re.findall(regexp, '\n'.join(ref_out)) if s != '']
    stu_match = [s for s in re.findall(regexp, '\n'.join(stu_out)) if s != '']
    if sort is True:
      ref_match = sorted(ref_match)
      stu_match = sorted(stu_match)
    if strict is False:
      ref_match = [re.sub(r'\s+', ' ', s) for s in ref_match]
      stu_match = [re.sub(r'\s+', ' ', s) for s in stu_match]
    if ref_match == stu_match:
      return (1, 0, stat.STAT_OK)
    else:
      return (0, 0, stat.STAT_DIFF)
