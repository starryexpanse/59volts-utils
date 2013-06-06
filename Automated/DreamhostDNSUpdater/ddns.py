#!/usr/bin/python -O

import json
import os
import re
import sys
import urllib2
from dreampylib import DreampyLib
import subprocess

CONF_PATH = '/etc/dreamhostdns.conf'


def getIP(ip_sources):
    proc = subprocess.Popen(['ifconfig'], stdout=subprocess.PIPE)
    proc.wait()
    out = proc.stdout.read()

    reviver = lambda x: x  # Todo read from file

    success = False
    for source in ip_sources:
        try:
            r = urllib2.urlopen(source['url'], timeout=50)
            ip = r.read()
            r.close()
        except urllib2.URLError:
            continue

        if r.getcode() == 200:
            success = True
            break

    if not success:
        raise Exception("Could not determine IP address (no sources available).")

    return ip

def main():
    global CONF_PATH

    if not os.path.isfile(CONF_PATH):
        sys.stderr.write("No configuration file ("+CONF_PATH+") found. Exiting." + os.linesep)
        sys.exit(1)

    h = open(CONF_PATH, "r")
    config = json.load(h)
    h.close()

    APIUSER = config.get("API Username")
    APIKEY = config.get("API Key")
    HOSTS = config.get("Hosts", [])

    IP = getIP(config["IP Echo Sources"]).strip()
    print "DEBUG: IP is", IP

    conn = getConn(APIUSER, APIKEY)

    for host in HOSTS:
        for record in conn.dns.list_records():
            if not (record['record'] == host and record['type'] == 'A'):
                continue
            if record['value'] == IP:
                if __debug__:
                    print "Old record for %(record)s found with IP %(value)s, no update needed." % record
                continue
            if __debug__:
                print "Old record for %(record)s found with IP %(value)s, removing." % record
            result = conn.dns.remove_record(
                record=record['record'],
                type=record['type'],
                value=record['value'],
            )
            if not conn.Status() == 'success':
                print "Warning: Old record NOT removed."
                continue

            print "Adding new record for %s with IP %s." % (host, IP)
            result = conn.dns.add_record(
                comment='Dynamic DNS IP',
                record=host,
                type='A',
                value=IP,
            )

            status = conn.Status()

            if not status == 'success':
                print "Warning: New record NOT added for %s. (Status=%s)" % (host, status)
            elif __debug__:
                print "Notice: Successfully added new record." % host

dns_records = None
def getRecords(ip, conn, hostname):
    global dns_records
    if dns_records is None:
        dns_records = conn.dns.list_records()
    return dns_records

def getConn(username, apikey):
        con = DreampyLib(username, apikey)
        if con.IsConnected():
            return con
        else:
            sys.exit("Could not connect to Dreamhost (invalid credentials perhaps?).")

if __name__ == "__main__":
    main()
