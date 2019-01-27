"""Compare status constants."""

STAT_OK = 'OK'            # Passed.
STAT_TIMEOUT = 'Time out' # Time limit exceeded.
STAT_MEMOUT = 'Mem out'   # Memory limit exceeded.
STAT_DIFF = 'Diff'        # Output different from reference.
STAT_PENALTY = 'Penalty'  # Time/performance not good enough.
STAT_MISSING = 'Missing'  # Missing output (maybe timeout on previous command).
STAT_NOFILE = 'No file'   # No output file.
STAT_ERROR = 'Error'      # Other errors set by evaluate functions.
STAT_BLOCKED = 'Blocked'  # Not scored because some other testcases fail.
