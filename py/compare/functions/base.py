"""Base class for compare classes."""

import dsnp_setting as dsnp
from compare import stat

class BaseCmp(object):
  def evalCmd(self, orig_score, orig_penalty, orig_status,
              full_score, ref_out, stu_out, **kargs):
    """Compare cmd outputs and update score and status."""
    val, penalty, status = self.cmpCmd(ref_out, stu_out, **kargs)
    # Update score and status
    new_score = self.updateScore(orig_score, full_score, val)
    new_penalty = self.updatePenalty(orig_penalty, penalty)
    new_status = self.updateStatus(orig_status, status)
    return (new_score, new_penalty, new_status)

  def evalMisc(self, orig_score, orig_penalty, orig_status,
               full_score, **kargs):
    """Misc compare and update score and status."""
    val, penalty, status = self.cmpMisc(**kargs)
    # Update score and status
    new_score = self.updateScore(orig_score, full_score, val)
    new_penalty = self.updatePenalty(orig_penalty, penalty)
    new_status = self.updateStatus(orig_status, status)
    return (new_score, new_penalty, new_status)

  def cmpCmd(self, ref_out, stu_out):
    """Compare ref output and student output."""
    raise NotImplementedError()

  def cmpMisc(self):
    """Misc compare."""
    raise NotImplementedError() 

  def updateScore(self, orig_score, full_score, val):
    """Update score."""
    return orig_score + full_score * val

  def updatePenalty(self, orig_penalty, penalty):
    """Update penalty."""
    return min(1.0, orig_penalty + penalty)

  def updateStatus(self, orig_status, status):
    """Update status."""
    return status if orig_status == stat.STAT_OK else orig_status
