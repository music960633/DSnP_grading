# DSnP grading system

A grading system for NTUEE DSnP course.

## Structure
The grading system contains the following directories:

* *py/* : The grading Python scripts.
* *testcase/* : Testcases and config files.
* *ref/* : Reference program.
* *student/* : Student programs, each in a separate directory
  *student/&lt;student_id&gt;&lt;hw_suffix&gt;*
  (e.g. *student/b01234567_fraig/*).

## Preparation
Before grading, these files should be prepared:

* Modify constants in *py/dsnp_setting.py* (*HW_SUFFIX*, *REF_EXE*,
  *STUDENT_EXE* and *PROMPT*)
* Put the reference program in *ref/ directory*. The executable should be
  *ref/&lt;ref_exe&gt;*. The default ref program *ref/fraig-ref* is an older
  Linux version of fraig. Change it if you are using macOS or want to use the
  latest version.
* Put the student programs in *student/&lt;student_id&gt;&lt;hw_suffix&gt;*
  directory. The executables should be
      *student/&lt;student_id&gt;&lt;hw_suffix&gt;/&lt;student_exe&gt;*
* Put the testdata in *testdata/dofile/* directory, and put the corresponding
  config files in *testdata/config/* directory. The config of dofile
  *&lt;dofile&gt;* is *&lt;dofile&gt;.json*
* Put the list of testcase names in a JSON file, e.g. *case_list.json*
* Put the list of student IDs in a JSON file, e.g. *student_list.json*

(Actually you can change the directory structure, just remember to change the
path in *py/dsnp_setting.py* as well.)

## Grading flow
There are three steps in the grading process

1. Generate reference outputs by running reference program on all testcases.
   ```
   py/runRef.py <case_list.json> [-p parallel_num]
   ```
   e.g. Run reference program with single core:
   ```
   py/runRef.py testcase/case_list.json
   ```
   It will create *ref_out/* directory and store the reference outputs in it.

2. Generate student outputs by running student programs on all testcases.
   ```
   py/runStudent.py <case_list.json> <student_list.json> [-p parallel_num]
   ```
   e.g. Run student programs with 5 cores:
   ```
   py/runStudent.py testcase/case_list.json student/student_list.json -p 5
   ```
   It will create *student_out/* directory and store the student outputs in
   *student_out/&lt;student_id&gt;*.

3. Compare the reference output and student output, generate scores for each
   students depending on the configs, and write to *&lt;score.csv&gt;* in CSV
   format.
   ```
   py/runScore.py <case_list.json> <student_list.json> <score.csv>
   ```
   e.g. Generate the scores into *result.csv*:
   ```
   py/runScore.py testcase/case_list.json student/student_list.json result.csv
   ```
