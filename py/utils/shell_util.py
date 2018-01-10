import os
import subprocess
import shutil

def copyAllFilesToDir(ref_dir, target_dir):
  """Copy all normal files in ref_dir to target_dir."""
  files = os.listdir(ref_dir)
  for f in files:
    ref_path = os.path.join(ref_dir, f)
    target_path = os.path.join(target_dir, f)
    if os.path.isfile(ref_path):
      shutil.copyfile(ref_path, target_path)


def removeDupFilesInDir(ref_dir, target_dir):
  """Remove all normal files in target_dir that appears in ref_dir."""
  files = os.listdir(ref_dir)
  for f in files:
    ref_path = os.path.join(ref_dir, f)
    target_path = os.path.join(target_dir, f)
    if os.path.isfile(ref_path) and os.path.isfile(target_path):
      os.remove(target_path)


def getMemUsage(pid):
  """Get process current memory usage."""
  mem_usage = 0
  try:
    out = subprocess.check_output(['ps', 'u', '-p', str(pid)]).splitlines()
    assert len(out) == 2, 'Unexpected "ps" output.'
    out[0] = out[0].split()
    out[1] = out[1].split()
    # Assume all strings except 'COMMAND' do not contain spaces
    assert 'RSS' in out[0], '"ps" output does not have "RSS" field.'
    idx = out[0].index('RSS')
    mem_usage = int(out[1][idx])
  except subprocess.CalledProcessError:
    pass
  return mem_usage


def checkMemProbe():
  """Check if memory usage can be probed."""
  pid = os.getpid()
  return getMemUsage(pid) != 0
