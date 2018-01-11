#!/bin/bash

cd `dirname $0`
cd ..

echo "# Write domains or subdomains you want not to crawl" > txt/blacklist.txt
echo "# Write IPv4 addresses you want not to crawl" > txt/ip_ban_list.txt
