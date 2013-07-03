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

from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.template import defaultfilters


from horizon import tables

from openstack_dashboard import api

################################################################################
# Server tables
class CreateServerAction(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Server")
    url = "horizon:dns:domains:server_create"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK CREATE SERVER"
        #return api.keystone.keystone_can_edit_user()
        return True

class EditServerAction(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:dns:domains:server_update"
    classes = ("ajax-modal", "btn-edit")

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK EDIT ACTION"
        #return api.keystone.keystone_can_edit_user()
        return True


class DeleteServerAction(tables.DeleteAction):
    data_type_singular = _("Server")
    data_type_plural = _("Servers")

    def allowed(self, request, datum):
        #if not api.keystone.keystone_can_edit_user() or \
        #        (datum and datum.id == request.user.id):
        #    return False
        #return True
        #TODO:
        print "TODO: CHECK DELETE SERVERS ACTION"
        return True

    def delete(self, request, domain_id):
        #TODO:
        print "TODO: DELETE SERVERS ACTION"
        api.moniker.server_delete(request, domain_id)

class AdminServersTable(tables.DataTable):
    name =  tables.Column("name",  verbose_name = _("Server name"))

    class Meta:
        name = "servers"
        verbose_name = _("Servers")

        table_actions = (CreateServerAction, DeleteServerAction,)
        row_actions   = (EditServerAction, DeleteServerAction,)

################################################################################
# Domain tables
class CreateDomainAction(tables.LinkAction):
    name = "create"
    verbose_name = _("Create Domain")
    url = "horizon:dns:domains:create"
    classes = ("ajax-modal", "btn-create")

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK CREATE DOMAIN"
        #return api.keystone.keystone_can_edit_user()
        return True

class EditDomainAction(tables.LinkAction):
    name = "edit"
    verbose_name = _("Edit")
    url = "horizon:dns:domains:update"
    classes = ("ajax-modal", "btn-edit")

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK EDIT ACTION"
        #return api.keystone.keystone_can_edit_user()
        return True

class DeleteDomainsAction(tables.DeleteAction):
    data_type_singular = _("Domain")
    data_type_plural = _("Domains")

    def allowed(self, request, datum):
        #if not api.keystone.keystone_can_edit_user() or \
        #        (datum and datum.id == request.user.id):
        #    return False
        #return True
        #TODO:
        print "TODO: CHECK DELETE DOMAINS ACTION"
        return True

    def delete(self, request, domain_id):
        #TODO:
        print "TODO: DELETE DOMAINS ACTION"
        api.moniker.domain_delete(request, domain_id)

class DomainFilterAction(tables.FilterAction):
    def filter(self, table, domains, filter_string):
        """ Naive case-insensitive search """
        q = filter_string.lower()
        return [domain for domain in domains
                if q in domain.name.lower()
                or q in domain.admin.lower()]

class EditDomainRecordsAction(tables.LinkAction):
    """
    Link to Records table
    """
    name = "edit_records"
    verbose_name = _("Edit Records")
    url = "horizon:dns:domains:records"
    #classes = ("ajax-modal", "btn-edit")

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK EDIT ACTION"
        #return api.keystone.keystone_can_edit_user()
        return True

class AdminDomainsTable(tables.DataTable):
    #id    = tables.Column("id")
    name  = tables.Column("name",  verbose_name = _("Domain name") , link = ("horizon:dns:domains:detail"))
    admin = tables.Column("admin", verbose_name = _("Admin e-mail"), filters=[defaultfilters.urlize])
    ttl   = tables.Column("ttl",   verbose_name = _("Time To Live"))

    class Meta:
        name = "domains"
        verbose_name = _("Domains")

        table_actions = (DomainFilterAction, CreateDomainAction, DeleteDomainsAction,)
        row_actions   = (EditDomainAction, EditDomainRecordsAction, DeleteDomainsAction,)

################################################################################
# Record tables
class CreateRecordAction(tables.LinkAction):
    name = "record_create"
    verbose_name = _("Create Record")
    url = "horizon:dns:domains:record_create"
    classes = ("ajax-modal", "btn-create")

    def get_link_url(self):
        domain_id = self.table.kwargs['domain_id']
        try:
            print "ADDR: %s" % reverse(self.url, args=(domain_id,))
        except Exception,e:
            print "Exception: %s" % e
            return "horizon:dns:domains:index"
        return reverse(self.url, args=(domain_id,))

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK CREATE RECORD"
        #return api.keystone.keystone_can_edit_user()
        return True


class EditRecordAction(tables.LinkAction):
    name = "record_update"
    verbose_name = _("Update record")
    url = "horizon:dns:domains:record_update"
    classes = ("ajax-modal", "btn-edit")

    def get_link_url(self, record):
        domain_id = self.table.kwargs['domain_id']
        print "ADDR: %s" % reverse(self.url, args=(domain_id, record.id))
        return reverse(self.url, args=(domain_id, record.id))

    def allowed(self, request, user):
        # TODO:
        print "TODO: CHECK EDIT ACTION"
        #return api.keystone.keystone_can_edit_user()
        return True

class DeleteRecordAction(tables.DeleteAction):
    data_type_singular = _("Record")
    data_type_plural = _("Records")

    def allowed(self, request, datum):
        #if not api.keystone.keystone_can_edit_user() or \
        #        (datum and datum.id == request.user.id):
        #    return False
        #return True
        #TODO:
        print "TODO: CHECK DELETE RECORDS ACTION"
        return True

    def delete(self, request, record_id):
        #TODO:
        print "TODO: DELETE RECORDS ACTION"
        domain_id = self.table.kwargs['domain_id']
        api.moniker.domain_delete(request, domain_id, record_id)


class RecordsFilterAction(tables.FilterAction):
    def filter(self, table, records, filter_string):
        """ Naive case-insensitive search """
        q = filter_string.lower()
        return [record for record in records
                if q in record.name.lower()
                or q in record.type.lower()]

class AdminDomainRecordsTable(tables.DataTable):
    #id = tables.Column("id", verbose_name = _("ID"))
    rec_type = tables.Column("rec_type", verbose_name = _("Type"))
    name     = tables.Column("name",     verbose_name = _("Record name"))
    value    = tables.Column("data",     verbose_name = _("Value"))
    priority = tables.Column("priority", verbose_name = _("Prority"))
    ttl      = tables.Column("ttl",      verbose_name = _("TTL"))

    class Meta:
        name = "records"
        verbose_name = _("Records")

        table_actions = (RecordsFilterAction, CreateRecordAction, DeleteRecordAction, )
        row_actions   = (EditRecordAction, DeleteRecordAction,)
