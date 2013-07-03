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

import logging

from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tables
from horizon import forms
from horizon import tabs

from openstack_dashboard import api
from .tables import (AdminDomainsTable,
                     AdminServersTable,
                     AdminDomainRecordsTable)
from .forms import (AdminCreateServerForm,
                    AdminUpdateServerForm,
                    AdminCreateDomainForm,
                    AdminUpdateDomainForm,
                    AdminCreateRecordForm,
                    AdminUpdateRecordForm)
from .tabs import DomainDetailTabs


LOG = logging.getLogger(__name__)

################################################################################
# Server views
class CreateServerView(forms.ModalFormView):
    form_class  = AdminCreateServerForm
    template_name = 'dns/domains/server_create.html'
    success_url = reverse_lazy('horizon:dns:domains:index')

    def dispatch(self, *args, **kwargs):
        return super(CreateServerView, self).dispatch(*args, **kwargs)

class UpdateServerView(forms.ModalFormView):
    template_name = 'dns/domains/server_update.html'
    form_class = AdminUpdateServerForm
    success_url = reverse_lazy('horizon:dns:domains:index')

    def dispatch(self, *args, **kwargs):
        return super(UpdateServerView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print "GET UPDATE CONTEXT"
        context = super(UpdateServerView, self).get_context_data(**kwargs)
        context['server_id'] = self.kwargs['server_id']
        return context

    def get_initial(self):
        print "[UpdateServerView::get_initial] kwargs:%s" % self.kwargs
        server = api.moniker.server_get(self.kwargs['server_id'])
        return server

################################################################################
# Domain views
class IndexView(tables.MultiTableView):
    table_classes   = (AdminDomainsTable, AdminServersTable)
    template_name = 'dns/domains/index.html'

    def get_servers_data(self):
        servers = []
        try:
            servers = api.moniker.server_list(self.request)
        except:
            msg = _('Unable to retrieve server list.')
            exceptions.handle(self.request, msg)
        return servers

    def get_domains_data(self):
        domains = []
        try:
            domains = api.moniker.domain_list(self.request)
        except:
            msg = _('Unable to retrieve domain list.')
            exceptions.handle(self.request, msg)
        return domains


class CreateView(forms.ModalFormView):
    form_class  = AdminCreateDomainForm
    template_name = 'dns/domains/create.html'
    success_url = reverse_lazy('horizon:dns:domains:index')

    def dispatch(self, *args, **kwargs):
        return super(CreateView, self).dispatch(*args, **kwargs)

class UpdateView(forms.ModalFormView):
    template_name = 'dns/domains/update.html'
    form_class = AdminUpdateDomainForm
    success_url = reverse_lazy('horizon:dns:domains:index')

    def dispatch(self, *args, **kwargs):
        return super(UpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print "GET UPDATE CONTEXT"
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['domain_id'] = self.kwargs['domain_id']
        return context

    def get_initial(self):
        print "[UpdateView::get_initial] kwargs:%s" % self.kwargs
        domain = api.moniker.domain_get(self.request, self.kwargs['domain_id'])
        return domain

class DetailView(tabs.TabView):
    tab_group_class = DomainDetailTabs
    template_name = 'dns/domains/detail.html'

################################################################################
# Record views

class RecordsView(tables.DataTableView):
    table_class   = AdminDomainRecordsTable
    template_name = 'dns/domains/record_index.html'

    def get_data(self):
        print "[RecordsView::get_data] self.kwargs: %s" % self.kwargs
        records = []
        try:
            records = api.moniker.records_list(self.request, self.kwargs['domain_id'])
        except:
            msg = _('Unable to retrieve records list.')
            exceptions.handle(self.request, msg)
        return records

class CreateRecordView(forms.ModalFormView):
    form_class  = AdminCreateRecordForm
    template_name = 'dns/domains/record_create.html'
    success_url = 'horizon:dns:domains:records'

    def get_success_url(self):
        domain_id = self.kwargs['domain_id']
        print "[CreateRecordView::get_success_url] domain_id: %s" % domain_id
        return reverse_lazy(self.success_url, args=(domain_id,))

    def dispatch(self, *args, **kwargs):
        print "[CreateRecordView::dispatch]"
        return super(CreateRecordView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print "[CreateRecordView::get_context_data]"
        context = super(CreateRecordView, self).get_context_data(**kwargs)
        context['domain_id'] = self.kwargs['domain_id']
        context['id'] = self.kwargs['domain_id']
        print "CONTEXT: %s" % context
        return context

    def get_initial(self):
        print "[CreateRecordView::get_initial]self.kwargs:%s" % self.kwargs
        #domain = api.moniker.record_get(self.request,
        #                                self.kwargs['domain_id'],
        #                                self.kwargs['record_id'])
        initial = {'domain_id' : self.kwargs['domain_id'],
                   'id'        : self.kwargs['domain_id'],
                   }
        return initial #domain

class UpdateRecordView(forms.ModalFormView):
    template_name = 'dns/domains/record_update.html'
    form_class = AdminUpdateRecordForm
    success_url = 'horizon:dns:domains:records'

    def get_success_url(self):
        domain_id = self.kwargs['domain_id']
        print "[UpdateRecordView::get_success_url] domain_id: %s" % domain_id
        return reverse_lazy(self.success_url, args=(domain_id,))

    def dispatch(self, *args, **kwargs):
        print "[UpdateRecordView::dispatch]"
        return super(UpdateRecordView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        print "[UpdateRecordView::get_context_data]"
        context = super(UpdateRecordView, self).get_context_data(**kwargs)
        context['domain_id'] = self.kwargs['domain_id']
        context['record_id'] = self.kwargs['record_id']
        return context

    def get_initial(self):
        print "[UpdateRecordView::get_initial]self.kwargs:%s" % self.kwargs
        domain = api.moniker.record_get(self.request,
                                        self.kwargs['domain_id'],
                                        self.kwargs['record_id'])
        return domain
