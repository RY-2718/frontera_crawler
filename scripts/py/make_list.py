# -*- coding: utf-8 -*-
import re

def blacklist(file_name):
  blacklist = set()
  with open(file_name,'r') as f:
    for row in f:
      s = row.strip()
      if len(s) > 0:
        if s[0] == "#":
          s = s[1:]
          #print("debug: %s" % s)
        blacklist.add(".*[\./]" + s + "[/]?")
  return blacklist

def new_list(blist_name, tmp_name):
  blist = blacklist(blist_name)
  with open(tmp_name, 'r') as f:
    for row in f:
      domainIsNew = True
      s = row.strip()
      for b in blist:
        if re.search(b, "/" + s) is not None:
          domainIsNew = False
          break

      if domainIsNew:
        print(s)
  return

if __name__ == '__main__':
  import sys
  argv = sys.argv
  argc = len(argv)

  if argc != 3:
    quit()

  new_list(argv[1], argv[2])

