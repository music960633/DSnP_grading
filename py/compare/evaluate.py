"""Read config file and use specified compare method for scoring."""

import os
import sys
import json

import dsnp_setting as dsnp
from compare import stat
from compare.functions import base

class Evaluator:
  """Compares a student output file for a dofile with ref output file, and
  calculates the total score.
  """
  def __init__(self, student, case):
    self.stu = student
    self.case = case
    self.ref_out_path = os.path.join(dsnp.REF_OUT_DIR, case + dsnp.OUT_SUFFIX)
    self.stu_out_path = os.path.join(dsnp.STU_OUT_DIR, student,
                                     case + dsnp.OUT_SUFFIX)
    self.config_path = os.path.join(dsnp.CONFIG_DIR, case + dsnp.JSON_SUFFIX)
    assert os.path.exists(self.ref_out_path), (
        'Ref output of %s does not exist!' % self.case)
    assert os.path.exists(self.config_path), (
        'Config file of %s does not exist!' % self.case)

  def getScoreAndStatus(self):
    return (self.tot_score, self.tot_status)

  def initialize(self):
    self.tot_score = 0
    self.tot_status = stat.STAT_OK
    self.eval_results = []
    self.label_map = {}

  def checkConsistency(self, sub_config, ref_sub_out, stu_sub_out):
    if '__cmd' in sub_config:
      prompt_cmd = dsnp.PROMPT + ' ' + sub_config['__cmd']
      assert ref_sub_out[0] == prompt_cmd
      assert stu_sub_out[0] == prompt_cmd

  def runDofileScore(self):
    """Calculates the total score, status for a dofile output and store them
    in self.tot_score, self.tot_status.
    """
    self.initialize()
    # No student output
    if not os.path.exists(self.stu_out_path):
      self.tot_status = stat.STAT_NOFILE
      return
    # Read config and check must exist fields
    with open(self.config_path) as f:
      config = json.load(f)
    checkConfig(config)
    # get output separated by prompt
    ref_out = readAndSplitByPrompt(self.ref_out_path, dsnp.PROMPT)
    stu_out = readAndSplitByPrompt(self.stu_out_path, dsnp.PROMPT)
    eval_list = config['evalList']
    assert len(ref_out) == len([c for c in eval_list if c['type'] == 'cmd']), (
        'Size of dofile and cmd config do not match')
    # score each command
    cmd_idx = 0
    for eval_config in eval_list:
      cls = getCmpClass(eval_config['method'])
      kargs = eval_config.get('args', {})
      if eval_config['type'] == 'cmd':
        # special case: missing output (e.g. segment fault). timeout and memout
        if cmd_idx >= len(stu_out):
          eval_result = (0, 0, stat.STAT_MISSING)
        elif 'TIMEOUT' in stu_out[cmd_idx]:
          eval_result = (0, 0, stat.STAT_TIMEOUT)
        elif 'MEMOUT' in stu_out[cmd_idx]:
          eval_result = (0, 0, stat.STAT_MEMOUT)
        else:
          # check consistency
          self.checkConsistency(eval_config, ref_out[cmd_idx], stu_out[cmd_idx])
          # use given method to evaluate
          eval_result = cls.evalCmd(
              eval_config['score'], ref_out[cmd_idx], stu_out[cmd_idx], **kargs)
          cmd_idx += 1
      elif eval_config['type'] == 'misc':
        # special field: 'need_ref_dir', 'need_stu_dir'
        if eval_config.get('need_ref_dir', False) is True:
          kargs.update({'ref_dir': dsnp.REF_OUT_DIR})
        if eval_config.get('need_stu_dir', False) is True:
          kargs.update({'stu_dir': os.path.join(dsnp.STU_OUT_DIR, self.stu)})
        # use given method to evaluate
        eval_result = cls.evalMisc(eval_config['score'], **kargs)

      self.updateResult(eval_config, eval_result)
      self.setLabel(eval_config, eval_result)

    # calculate total score
    self.calcTotScore()

  def updateResult(self, config, result):
    """Append a result dict to eval_results."""
    require = config.get('require', [])
    if isinstance(require, basestring):
      require = [require]
    result_dict = {
        'result': result,
        'require': require
    }
    self.eval_results.append(result_dict)

  def setLabel(self, config, result):
    """Insert a label to label_map."""
    if 'label' in config:
      label = config['label']
      assert'label' not in self.label_map, 'Duplicate label %s' % label
      self.label_map[label] = result

  def calcTotScore(self):
    """Calculate final score."""
    tot_penalty = 0
    for result_dict in self.eval_results:
      score, penalty, status = result_dict['result']
      require = result_dict['require']
      if all([self.label_map[label][2] == stat.STAT_OK for label in require]):
        self.tot_score += score
        tot_penalty = min(1.0, tot_penalty + penalty)
        if self.tot_status == stat.STAT_OK:
          self.tot_status = status

    # apply penalty
    if tot_penalty > 0:
      # status can be penalty only if all the tests passed
      if self.tot_status == stat.STAT_OK:
        self.tot_status = stat.STAT_PENALTY
      self.tot_score *= (1 - tot_penalty)
      self.tot_score = int(self.tot_score + 0.5)


def checkConfig(config):
  """Checks the config that
    1. 'timelimit' must exist in config.
    2. 'evalList' must exist in config.
    3. For each subconfigs in 'evalList' for subcommands:
      a. 'type', 'score', 'method' must exist in subconfig.
      b. type of subconfig should be either 'cmd' or 'misc'.
    4. Should not have duplicate labels, and 'require' should not contain
       unknown labels.
  """
  for key in ['timelimit', 'evalList']:
    assert key in config, (
        'Missing "%s" in config "%s".' % (key, os.path.basename(config_path)))
  for eval_config in config['evalList']:
    for key in ['type', 'score', 'method']:
      assert key in eval_config, (
          'Missing "%s" in config "%s".' % (key, os.path.basename(config_path)))
    assert eval_config['type'] in ['cmd', 'misc'], (
        'Unknown eval type: %s.' % eval_config['type'])
  label_set = set()
  for eval_config in config['evalList']:
    if 'label' in eval_config:
      label = eval_config['label']
      assert label not in label_set, (
          'Duplicate label %s.' % label)
      label_set.add(label)
    require = eval_config.get('require', [])
    if isinstance(require, basestring):
      require = [require]
    for label in require:
      assert label in label_set, 'Unknown require label %s.' % label


def readAndSplitByPrompt(filename, prompt):
  """Read a file and transform into a list of lists of strings. Strings are
  rstrip-ed, and the first string of a sublist starts with `prompt`. For
  example, if `prompt` is 'fraig>' and the file content is

    fraig> cirread test.aag\n
    Reading...   \n
    fraig> cirprint\n
      meow meow\n
    fraig> q -f

  then the returned list is

    [
      ['fraig> cirread test.aag', 'Reading...'],
      ['fraig> cirptint', '  meow meow'],
      ['fraig> q -f']
    ]
  """
  ret = []
  with open(filename, 'r') as f:
    for s in f:
      s = s.rstrip()
      if s.startswith(prompt):
        ret.append([s])
      elif s != '':
        # special case: killed before output anything
        if len(ret) == 0 and (s == 'TIMEOUT' or s == 'MEMOUT'):
          ret.append([])
        ret[-1].append(s)
  return ret


def getCmpClass(cmp_name):
  """Get compare class from given method."""
  module_name = dsnp.CMP_MODULE_PREFIX + '.' + cmp_name
  try:
    cmp_module = __import__(module_name, globals(), locals(), ['meow'], -1)
  except ImportError:
    raise Exception('Error importing module "%s"' % module_name)
  for key, val in cmp_module.__dict__.iteritems():
    if isinstance(val, type) and issubclass(val, base.BaseCmp):
      return val()
  raise Exception('No compare class found in module "%s"' % module_name)
