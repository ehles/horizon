# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 ASD Technologies, asdco.ru.
#
# Author: Denis Deryabin <dderyabin@asdco.ru>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from __future__ import absolute_import

import itertools
import logging
import thread
import urlparse

from django.conf import settings

LOG = logging.getLogger(__name__)

################################################################################
# FOR DEBUG
DOMAINS = []
SERVERS = []
class Server:
    counter = 0
    def __init__(s):
        Server.counter += 1
        s.id = "S-%d-S" % Server.counter
        s.name = "server_name_%d" % Server.counter


class Record:
    counter = 0
    def __init__(s):
        Record.counter+=1

        s.id = "R-%d-R" % Record.counter
        s.name = ""
        s.type = None
        s.data = None
        s.priority = 0

    def init(s, data):
        #s.id       = data['id']
        s.name     = data['name']
        s.rec_type = data['rec_type']
        s.data     = data['data']
        s.ttl      = 5000
        s.priority = 1

    def as_dict(s):
        return {
            'id'       : s.id,
            'name'     : s.name,
            'rec_type' : s.rec_type,
            'data'     : s.data,
            'ttl'      : s.ttl,
            'priority' : s.priority
        }

class Domain:
    counter =  0
    def __init__(s):
        Domain.counter += 1
        s.records_list = []
        s.id    = "D-%d-D" % (Domain.counter)
        s.name  = ""
        s.admin = ""
        s.ttl   = ""

    def init(s, data):
        #s.id    = data['id']
        s.name  = data['name']
        s.admin = data['admin']
        s.ttl   = data['ttl']
        return s

    def add_record(s, name, rec_type, value):
        rec = Record()
        rec.init({  # 'id'        : "R-%d-R" % (len(s.records_list) + 1),
                   #'domain_id' : "test",
                   'name'      : "%s_.%s" % (s.name, name),
                   'rec_type'  : rec_type,
                   'data'      : value
                   })
        s.records_list.append(rec)


    def as_dict(s):
        return {
            'id'    : s.id,
            'name'  : s.name,
            'admin' : s.admin,
            'ttl'   : s.ttl
        }

def xxx():
    try:
        for i in xrange(1,3):
            SERVERS.append(Server())
        for i in xrange(1, 10):
            d = Domain()
            data = {
                'name'  : "domain-%d" % i,
                'admin' : "admin%d@mail.ru" % i,
                'ttl'   : 7400
            }
            d.init(data)
            for j in xrange(2, 10):
                d.add_record("mail.example.com.",
                             "MX",
                             "mail%d.example.com." % j )
            DOMAINS.append(d)
    except Exception, e:
        print "Execption: %s" % e
        raise
    print "-"*50

xxx()


# FOR DEBUG
################################################################################
# Servers
def server_list(request):
    print("[server_list]")
    return SERVERS

def server_add(request, data):
    print("[server_add]")
    server = Server()
    server.name = data['name']
    SERVERS.append(server)

def server_get(server_id):
    print("[server_get]")
    for s in SERVERS:
        print ("Check server:%s" % s.id)
        if s.id == server_id:
            print ("Found:%s" % s.id)
            return {'name': s.name,
                    'id'  : s.id
            }
    else:
        print ("Not found:%s" % s.id)
        return None

def server_update(request, data):
    print("[server_update]")
    for i in range(len(SERVERS)):
        if SERVERS[i].id == data['id']:
            SERVERS[i].name = data['name']
            break
    else:
        print("[server_update] Server not found")

def server_delete(request, server_id):
    print("[server_delete]")
    for i in range(len(SERVERS)):
        if SERVERS[i].id == server_id:
            del(SERVERS[i])
            break
    else:
        print("[server_delete] Server not found")

################################################################################
def domain_create(request, data):
    """
    Creates new domain
    """
    # TODO:
    print "TODO: Create DOMAIN %s" % data
    d = Domain().init(data)
    DOMAINS.append(d)
    return d

def domain_list(request, marker=None, filters=None, paginate=False):
    """
    Gets domain list
    """
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit
    kwargs = {'filters': filters or {}}
    if marker:
        kwargs['marker'] = marker

    return DOMAINS


def domain_update(request, data):
    # TODO:
    print "TODO: Update DOMAIN %s" % data
    for d in DOMAINS:
        if d.id == data['id']:
            d.init(data)
            return
    else:
        print "[WARNING] domain not found"
        return

def domain_get(request, domain_id):
    # TODO:
    print "TODO: GET DOMAIN INFO FOR '%s'" % domain_id
    for d in DOMAINS:
        if d.id == domain_id:
            return d.as_dict()
    else:
        print "[WARNING] domain not found"
        return {}

def domain_delete(request, domain_id):
    # TODO:
    print "TODO: Delete domain id: %s" % domain_id
    for i in xrange(len(DOMAINS)):
        if DOMAINS[i].id == domain_id:
            del(DOMAINS[i])
            return
    else:
        print "[WARNING] domain not found"
        return

def records_list(request, domain_id, marker=None, filters=None, paginate=False):
    limit = getattr(settings, 'API_RESULT_LIMIT', 1000)
    page_size = getattr(settings, 'API_RESULT_PAGE_SIZE', 20)

    if paginate:
        request_size = page_size + 1
    else:
        request_size = limit
    kwargs = {'filters': filters or {}}
    if marker:
        kwargs['marker'] = marker
    print "GET RECORDS LIST FOR DOMAIN:%s" % domain_id
    for d in DOMAINS:
        if d.id == domain_id:
            #print "return :%s" %  d.records_list
            return d.records_list
    return []

def record_get(request, domain_id, record_id):
    print "TODO: GET RECORD INFO FOR DOMAIN id'%s', record_id:%s" % (domain_id, record_id, )
    for d in DOMAINS:
        if d.id == domain_id:
            break
    else:
        print "[WARNING] domain not found"
        return {}

    for r in d.records_list:
        print "record_id: '%s'; r.id:'%s'" % (record_id,r.id)
        if str(r.id) == str(record_id):
            res = r.as_dict()
            res['domain_id'] =  domain_id
            return res
    else:
        print "[WARNING] record not found"
        return {}

def record_update(request, data):
    # TODO:
    print "TODO: Update RECORD %s" % data
    for d in DOMAINS:
        print "check %s == %s " % (d.id, data['domain_id'], )
        if d.id == data['domain_id']:
            for r in d.records_list:
                if str(r.id) == str(data['id']):
                    r.init(data)
                    return
    else:
        print "[WARNING] record not found"
        return


def record_create(request, data):
    # TODO:
    print "TODO: Create RECORD %s" % data
    for d in DOMAINS:
        if d.id == data['id']:
            d.add_record(
                data['name'],
                data['rec_type'],
                data['data'],
                )
            return d
    else:
        print "[WARNING] domain not found"
        return data

def domain_delete(request, domain_id, record_id):
    # TODO:
    print "TODO: Delete RECORD %s, %s" % (domain_id, record_id, )
    for d in DOMAINS:
        print "check %s == %s " % (d.id, domain_id, )
        if d.id == domain_id:
            for i in xrange(len(d.records_list)):
                if str(d.records_list[i].id) == str(record_id):
                    del(d.records_list[i])
                    return
    else:
        print "[WARNING] record not found"
        return




