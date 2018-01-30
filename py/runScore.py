#!/usr/bin/python2.7

import argparse
import os
import sys
import json

import dsnp_setting as dsnp
from utils import parse_util
from compare import evaluate
from compare import stat

def normalize(case_list):
  for i, case in enumerate(case_list):
    if isinstance(case, basestring):
      case_list[i] = {
          'case': case,
          'require': []
      }
    elif isinstance(case['require'], basestring):
      case['require'] = [case['require']]


def genHeader(score_table, case_list):
  """Generate CSV header."""
  header = ['Student ID']
  for case_dict in case_list:
    header.append(case_dict['case'])
    header.append('Status')
  header.append('Total')
  score_table.append(header)


def genStudent(score_table, student, case_list):
  """Generate student scores by evaluating outputs."""
  score = [student]
  student_output_dir = os.path.join(dsnp.STU_OUT_DIR, student)
  # Get score for each case
  tot = 0
  status_dict = {}
  for case_dict in case_list:
    case = case_dict['case']
    require = case_dict['require']
    print '[%s] Scoring %s' % (student, case)
    passed = lambda status: status in [stat.STAT_OK, stat.STAT_PENALTY]
    if all([passed(status_dict[name]) for name in require]):
      evaluator = evaluate.Evaluator(student, case)
      evaluator.runDofileScore()
      val, status = evaluator.getScoreAndStatus()
    else:
      val, status = 0, stat.STAT_BLOCKED
    tot += val
    score.append(str(val))
    score.append(status)
    status_dict[case] = status
  score.append(str(tot))
  score_table.append(score)


def genMaxScore(score_table, case_list):
  """Generate max score for each dofiles."""
  header = ['Max score']
  tot_score = 0
  for case_dict in case_list:
    case = case_dict['case']
    config_path = os.path.join(dsnp.CONFIG_DIR, case + dsnp.JSON_SUFFIX)
    with open(config_path, 'r') as f:
      config = json.load(f)
    dofile_score = sum([subconfig.get('score', 0) for subconfig in config['evalList']])
    tot_score += dofile_score
    header.append(str(dofile_score))
    header.append('')
  header.append(str(tot_score))
  score_table.append(header)


def genScore(case_list, student_list):
  """Generate complete score table including header and scores."""
  score_table = []
  genHeader(score_table, case_list)
  for student in student_list:
    genStudent(score_table, student, case_list)
  genMaxScore(score_table, case_list)
  return score_table


def writeCsv(score_csv, score_table):
  """Write the score table to a CSV file."""
  with open(score_csv, 'w') as f:
    for score in score_table:
      f.write('%s\n' % ','.join(score))


def main():
  # Arguments
  parser = argparse.ArgumentParser(description='Get student scores.')
  parser.add_argument('case_list_json', type=str,
                      help='Filename for case list in JSON format')
  parser.add_argument('student_list_json', type=str,
                      help='Filename for student list in JSON format')
  parser.add_argument('score_csv', type=str,
                      help='Filename for output score csv')
  args = parser.parse_args()

  # Read case_list and student_list
  case_list = parse_util.parseJsonFromFile(args.case_list_json)
  normalize(case_list)
  student_list = parse_util.parseJsonFromFile(args.student_list_json)

  # generate score
  score_table = genScore(case_list, student_list)

  # write score to CSV
  writeCsv(args.score_csv, score_table)


if __name__ == '__main__':
  main()
