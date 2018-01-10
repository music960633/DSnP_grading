"""
Settings for DSnP grading scripts
Some need to be changed for each homeworks:
  HW_SUFFIX   : name of homework
  REF_EXE     : name of ref executable
  STU_EXE     : name of student executable
  PROMPT      : command line prompt
"""

import os
import sys

# homework suffix
HW_SUFFIX = '_fraig'

# name of executable
REF_EXE = 'fraig-ref'
STU_EXE = 'fraig'

# command line prompt
PROMPT = 'fraig>'

# file suffix
OUT_SUFFIX  = '.out'
JSON_SUFFIX = '.json'

# compare module path
CMP_MODULE_PREFIX = 'compare.functions'

# set root
ROOT = os.path.dirname(os.path.dirname(
    os.path.realpath(__file__.replace('.pyc', '.py'))))

# add ROOT to import path
if os.path.join(ROOT, 'py') not in sys.path:
  sys.path.append(os.path.join(ROOT, 'py'))

# absolute path directories
REF_DIR     = os.path.join(ROOT, 'ref')
REF_OUT_DIR = os.path.join(ROOT, 'ref_out')
STU_DIR     = os.path.join(ROOT, 'student')
STU_OUT_DIR = os.path.join(ROOT, 'student_out')
DOFILE_DIR  = os.path.join(ROOT, 'testcase', 'dofile')
CONFIG_DIR  = os.path.join(ROOT, 'testcase', 'config')
