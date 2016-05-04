#!/usr/bin/env python

copyright = """
Nagios nrpe plugins to check if some path exist files where mtime value
older than x seconds

Copyright (C) 2016 Pasi Lammi

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""

import string
import argparse
import glob
import os
import time
import sys

time_warning = 60*60*4
time_critical = 60*60*8

args = None

def read_args():
  global args
  p = argparse.ArgumentParser()
  p.add_argument('--file', help='specify full path of file(s)')
  p.add_argument('--warning', type=int, help='warning level on seconds (default:%s)' % time_warning, default=time_warning)
  p.add_argument('--critical', type=int, help='critical level on seconds (default:%s)' % time_critical, default=time_critical)
  args = p.parse_args()


def check_files():
  ret = { 'lines': [], 'status': 0 }
  t = time.time()
  global args
  if not args.file:
    return []
  files = glob.glob(args.file)
  for f in files:
    status = 0
    s = os.stat(f)
    m_time = s.st_mtime
    age = t - s.st_mtime
    if age > args.critical:
      status = 2
    elif age > args.warning:
      status = 1
    r = { 'status': status, 'age': int(age), 'file': f }
    ret['lines'].append(r)

    if status > ret['status']:
      ret['status'] = status

  return ret


def print_line(data):
  status = ['OK','WARNING','CRITICAL']
  lines = ["%s=%s" % (x['file'],x['age']) for x in data['lines']]
  print "%s: for files: %s" % (status[data['status']], string.join(lines))

if __name__ == "__main__":
  read_args()
  files = check_files()
  if len(files) == 0:
    print "OK: no files found"
    sys.exit(0)
  print_line(files)
  sys.exit(files['status'])
