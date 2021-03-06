#! /usr/bin/env python -vv
# Write a function that reads the /etc/hosts and return the hostname, given the ip address.
# From http://www.pyschools.com/quiz/view_question/s13-q10

import sys

def gethostname_split(ip_address):
  fh = open('/tmp/hosts', 'r')
  columns = {}
  for line in fh.readlines():
    if not line.startswith('#'):
      tokens = line.split()
      if len(tokens) > 1:
        columns[tokens[0]] = tokens[1]

  print columns
  try:
    return columns[ip_address]
  except KeyError:
    return 'Unknown host'

def gethostname_regex(ip_address):
  import re
  fh = open('/tmp/hosts', 'r')
  re = re.compile(r"^(\d+\.\d+\.\d+\.\d+)[ ]+([^ ]+)")

  columns = {}
  for line in fh.readlines():
    #return line
    if line[:1].isdigit():
      #return line
      #print re.match(line).groups()
      matches = re.match(line)
      if matches:
        values = matches.groups()
        columns[values[0]] = values[1]

  print columns
  try:
    return columns[ip_address].strip('\n')
  except KeyError:
    return 'Unknown host'

if len(sys.argv) < 2:
  print 'No IP provided. Looking up 127.0.0.1'
  print gethostname_regex('127.0.0.1')
  print gethostname_split('127.0.0.1')
else:
  print gethostname_regex(sys.argv[1])
  print gethostname_split(sys.argv[1])
