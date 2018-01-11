def blacklist(file_name):
  blacklist = set()
  with open(file_name,'r') as f:
    for row in f:
      s = row.strip()
      if len(s) > 0 and s[0] != "#":
        blacklist.add("[.\/]" + s + "[.\/]?$")
  return blacklist
