"""Compare class for "qualitypenalty" compare method."""

import re
import math

import dsnp_setting
from compare import stat
from compare.functions import base

_RE_TOTAL_GATE = re.compile(r'Total\s*(\d+)')
_QUALITY_PENALTY = lambda ref, stu, y: (math.sqrt(stu - ref) / y)

class QualityPenaltyCmp(base.BaseCmp):
  def cmpCmd(self, ref_out, stu_out, y=50):
    """Compare ref output and student output.

    Calculates a quality penalty depending on ref and student gate count.
    The mapping from student #gate (stu_gate) to penalty is:

      If stu_gate <= ref_gate, penalty = 0
      If stu_gate >  ref_gate, penalty = sqrt(stu_gate - ref_gate) / y

    Args:
      ref_out: Ref output in list of strings.
      stu_out: Student output in list of strings.
      y: Described above.

    Returns:
      Tuple (0, 1, stat.ERROR) if student time is not found. Otherwise return
      (0, penalty, status), where status is stat.STAT_PENALTY if penalty is
      greater than 0, otherwise stat.STAT_OK.

    """
    ref_result = _RE_TOTAL_GATE.search('\n'.join(ref_out))
    stu_result = _RE_TOTAL_GATE.search('\n'.join(stu_out))
    assert ref_result is not None, 'Cannot find total gate count in ref output.'
    if stu_result is None:
      return (0, 1, stat.STAT_ERROR)
    
    ref_gate = int(ref_result.group(1))
    stu_gate = int(stu_result.group(1))
    if stu_gate <= ref_gate:
      penalty = 0
    else:
      penalty = _QUALITY_PENALTY(ref_gate, stu_gate, y)
    
    status = stat.STAT_PENALTY if penalty > 0 else stat.STAT_OK
    return (0, penalty, status)
