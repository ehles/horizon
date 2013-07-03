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
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard.api import moniker


class OverviewTab(tabs.Tab):
    name = _("Overview")
    slug = "overview"
    template_name = "dns/domains/_detail_overview.html"

    def get_context_data(self, request):
        domain_id = self.tab_group.kwargs['domain_id']
        try:
            domain = moniker.domain_get(request, domain_id)
        except:
            redirect = reverse('horizon:dns:domains:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve domain details.'),
                              redirect=redirect)

        try:
            records = moniker.records_list(request, domain_id)
        except:
            redirect = reverse('horizon:dns:domains:index')
            exceptions.handle(self.request,
                              _('Unable to retrieve domain details.'),
                              redirect=redirect)

        print "RESULT: domain:%s, records:%s" % (domain, records, )
        return {'domain' : domain,
                'records': records,}


class DomainDetailTabs(tabs.TabGroup):
    slug = "domain_details"
    tabs = (OverviewTab, )
