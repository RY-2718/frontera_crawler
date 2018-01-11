# -*- coding: utf-8 -*-
import re
from six.moves.urllib.parse import urlparse
import gzip

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

def new_list(blist_name, gzip_name):
  blist = blacklist(blist_name)
  with gzip.open(gzip_name, 'rt') as f:
    for row in f:
      s = row.strip()
      if s[-4:] != 'html' or s[:5] != '2017-':
        continue
      url = s.split(" ")[2][:-1]
      domain = urlparse(url).netloc
      s3 = s.split(" ")[-1]
      for b in blist:
        if re.search(b, "/" + s) is not None:
          print(s3)
          break
  return

if __name__ == '__main__':
  import sys
  argv = sys.argv
  argc = len(argv)

  if argc != 3:
    print("usage: %s [domain list for delete from s3] [gzip file]" % (argv[0]))
    quit()

  new_list(argv[1], argv[2])

