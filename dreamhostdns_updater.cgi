#!/usr/bin/python3

import os
from uuid import uuid4 as uuid
import cgi
import requests

list_url = 'https://api.dreamhost.com/?key={apikey}&cmd=dns-list_records&unique_id={uuid}'
del_url = 'https://api.dreamhost.com/?key={apikey}&cmd=dns-remove_record&unique_id={uuid}&record={hostname}&type={recordtype}&value={old_addr}'
add_url = 'https://api.dreamhost.com/?key={apikey}&cmd=dns-add_record&unique_id={uuid}&record={hostname}&type={recordtype}&value={new_addr}&comment={comment}'

if __name__ == '__main__':
    print ("Content-Type: text/plain\n")
    form = cgi.FieldStorage ()
    d = dict()

    try:
        d['apikey'] = form["key"].value
        d['hostname'] = form["hostname"].value
        try:
            d['new_addr'] = form["address"].value
        except:
            d['new_addr'] = os.environ['REMOTE_ADDR']
        d['uuid'] = str(uuid())
        d['comment'] = 'Updated by OPNsense via dreamhostdns_updater.cgi'
        d['comment'] = d['comment'].replace (' ', '%20')
        d['recordtype'] = "A"
        r = requests.get (list_url.format (**d))
        for l in r.text.split ('\n'):
            fields = l.split ('\t')
            if len(fields) < 5:
                continue
            if fields[2] == d['hostname'] and fields[3] == d['recordtype']:
                d['old_addr'] = fields[4]
                if d['old_addr'] != d['new_addr']:
                    d['uuid'] = str(uuid())
                    if "testing" in form:
                        print (del_url.format (**d))
                    else:
                        r = requests.get (del_url.format (**d))
                    d['uuid'] = str(uuid())
                    if "testing" in form:
                        print (add_url.format (**d))
                    else:
                        r = requests.get (add_url.format (**d))
                break
        else:
            if "testing" in form:
                print (add_url.format (**d))
            else:
                r = requests.get (add_url.format (**d))

        print ("success : {hostname}".format (**d))
    except:
        print ("fail")
