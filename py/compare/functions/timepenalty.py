"""Compare class for "timepenalty" compare method."""

import re

import dsnp_setting
from compare import stat
from compare.functions import base

_RE_TOTAL_TIME = re.compile(r'Total time used\s*:\s*(\d*\.?\d+)\s*seconds')

class TimePenaltyCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out,
             min_val, max_val, min_penalty, max_penalty, relative=False):
    """Compare ref output and student output.

    Calculates a time penalty depending on ref and student time. The mapping
    from student time (stu_time) to penalty is:

      If stu_time <= min_time, penalty = `min_penalty`
      If stu_time >= max_time, penalty = `max_penalty`
      If min_time < stu_time < max_time, penalty increases linearly

    If `relative` is set to False, min_time, max_time are equivalent to
    `min_val` and `max_val`. If `relative` is set to True, min_time, max_time
    are `min_val`, `max_val` multiplied by ref time.

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.
      min_penalty: Described above.
      max_penalty: Descrived above.
      min_ratio: Described above.
      max_ratio: Descrived above.
      relative: Use relative time compared to ref time.

    Returns:
      Tuple (0, 1, stat.ERROR) if student time is not found. Otherwise return
      (0, penalty, status), where status is stat.STAT_PENALTY if penalty is
      greater than 0, otherwise stat.STAT_OK.

    """
    if relative is True:
      ref_result = _RE_TOTAL_TIME.search('\n'.join(ref_out))
      assert ref_result is not None, 'Cannot get ref time.'
      ref_time = float(ref_result.group(1))
      min_time = ref_time * min_val
      max_time = ref_time * max_val
    else:
      min_time = min_val
      max_time = max_val

    stu_result = _RE_TOTAL_TIME.search('\n'.join(stu_out))
    if stu_result is None:
      return (0, 1, stat.STAT_ERROR)
    
    stu_time = float(stu_result.group(1))
    if stu_time <= min_time:
      penalty = min_penalty
    elif stu_time >= max_time:
      penalty = max_penalty
    else:
      slope = float(max_penalty - min_penalty) / float(max_time - min_time)
      penalty = min_penalty + slope * (stu_time - min_time)
    
    status = stat.STAT_PENALTY if penalty > 0 else stat.STAT_OK
    return (0, penalty, status)
