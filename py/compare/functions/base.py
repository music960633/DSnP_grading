"""Base class for compare classes."""

import dsnp_setting as dsnp
from compare import stat

class BaseCmp(object):
  def evalCmd(self, full_score, ref_out, stu_out, **kargs):
    """Compare cmd outputs and update score and status."""
    val, penalty, status = self.cmpCmd(ref_out, stu_out, **kargs)
    return (val * full_score, penalty, status)

  def evalMisc(self, full_score, **kargs):
    """Misc compare and update score and status."""
    val, penalty, status = self.cmpMisc(**kargs)
    return (val * full_score, penalty, status)

  def cmpCmd(self, ref_out, stu_out):
    """Compare ref output and student output."""
    raise NotImplementedError()

  def cmpMisc(self):
    """Misc compare."""
    raise NotImplementedError() 
