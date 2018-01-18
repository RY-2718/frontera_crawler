import logging
import os
import re
from collections import deque
from crawler.blacklist import blacklist
from scrapy.exceptions import IgnoreRequest
from six.moves.urllib.parse import urlparse
from twisted.internet.error import DNSLookupError
from twisted.names import client, error

logging.config.fileConfig(fname="logging.conf", disable_existing_loggers=False)
middleware_logger = logging.getLogger("middleware_logger")
ip_logger = logging.getLogger("ip_logger")

class DenyBlacklistDomainMiddleware(object):
    deny_list = []

    blist = blacklist(os.path.dirname(os.path.abspath(__file__)) + '/../txt/blacklist.txt')
    deny_list.extend(blist)

    def process_request(self, request, spider):
        domain = urlparse(request.url).netloc
        for deny in self.deny_list:
            if re.search(deny, "/" + domain) is not None:
                middleware_logger.debug(request.url)
                raise IgnoreRequest
        return None

class ReturnQueryURLMiddleware(object):
    def process_request(self, request, spider):
        if len(urlparse(request.url).query) > 0 and (not request.meta.get("rescheduled")):
            request.meta["rescheduled"] = True
            return request
        return None

class DownloadTooMuchAtOnceCheckerMiddleware(object):
    def __init__(self):
        self.queue = deque([])
        self.size = 256
        self.threshold = 50

    def process_request(self, request, spider):
        domain = urlparse(request.url).netloc
        if len(self.queue) < self.size:
            self.queue.append(domain)
        else:
            if self.queue.count(domain) >= self.threshold and not request.meta.get("dupricated"):
                print("domain too dupricated: " + request.url)
                request.meta["rescheduled"] = True
                request.meta["dupricated"] = True
                return request
            else:
                self.queue.popleft()
                self.queue.append(domain)
        return None

class IPCheckerMiddleware(object):
    # hacked twisted
    def __init__(self):
        self.queue = deque([])
        self.size = 512
        self.threshold = 100
        self.already_logged_set = set()

        def get_ip_ban_list(filename):
            res = set()
            with open(filename, "r") as f:
                for row in f:
                    if len(row) > 0 and row[0] != '#':
                        res.add(row.strip())
                return res
    
        self.ip_ban_list = get_ip_ban_list(os.path.dirname(os.path.abspath(__file__)) + '/../txt/ip_ban_list.txt')

    def process_request(self, request, spider):
        def got_ip(address, hostname):
            if address in self.ip_ban_list:
                raise IgnoreRequest
            else:
                if len(self.queue) < self.size:
                    self.queue.append(address)
                else:
                    if self.queue.count(address) >= self.threshold:
                        if not address in self.already_logged_set:
                            self.already_logged_set.add(address)
                            print("IP too dupricated: %s, %s" % (hostname, address))
                            ip_logger.debug("%s, %s" % (hostname, address))
                    self.queue.popleft()
                    self.queue.append(address)
                return None
    
        def got_error(failure, hostname):
            failure.trap(error.DNSNameError, DNSLookupError)
            raise IgnoreRequest

        def tryV6(failure, hostname):
            dV6 = client.getHostByNameV6Address(hostname)
            dV6.addCallback(got_ip, hostname)
            dV6.addErrback(try6, hostname)
            return dV6

        def try6(failure, hostname):
            d6 = client.getHostByName6(hostname)
            d6.addCallback(got_ip, hostname)
            d6.addErrback(got_error, hostname)
            return d6
    
        hostname = urlparse(request.url).netloc
        d = client.getHostByNameV4(hostname)
        d.addCallback(got_ip, hostname)
        d.addErrback(tryV6, hostname)

        return d
