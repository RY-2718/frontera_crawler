# -*- coding: utf-8 -*-
import re
from six.moves.urllib.parse import urlparse
import sys

def blacklist(file_name):
  blacklist = set()
  with open(file_name,'r') as f:
    for row in f:
      s = row.strip()
      if len(s) > 0:
        if s[0] == "#":
          s = s[1:]
          #print("debug: %s" % s)
        blacklist.add(".*[\./]" + s + "[\./]?")
  return blacklist

def new_list(blist_name, tmp_name):
  blist = blacklist(blist_name)
  deny_list = ['category', 'page', 'tag', 'article', 'blog', '/fund/', '/news/', 'rakuten', 'calendar']
  with open(tmp_name, 'r') as f:
    for i, row in enumerate(f):
      if i % 1000 == 0:
        sys.stderr.write(str(i) + "th iteration\n")
      domainIsNew = True
      s = row.strip()
      s = s[s.find("http"):]
      domain = urlparse(s).netloc

      for d in deny_list:
        if d in s.lower():
          domainIsNew = False
          break
      if not domainIsNew:
        continue

      for b in blist:
        if re.search(b, "/" + domain) is not None:
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

