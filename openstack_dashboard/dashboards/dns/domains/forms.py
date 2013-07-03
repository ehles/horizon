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

from django.utils.translation import force_unicode, ugettext_lazy as _
from openstack_dashboard import api

from horizon import exceptions
from horizon import workflows
from horizon import messages
from horizon import forms

LOG = logging.getLogger(__name__)
################################################################################
# Server forms
class AdminCreateServerForm(forms.SelfHandlingForm):
    name  = forms.CharField(label=_("Server name"))

    def handle(self, request, data):
        try:
            LOG.info('Creating server "%s"' % data['name'])
            new_server = api.moniker.server_add(request, data)
            messages.success(request, _('Server "%s" successfully created.' % data['name']))
        except:
            exceptions.handle(request, "Unable to create server")
        return True

class AdminUpdateServerForm(forms.SelfHandlingForm):
    id    = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    name  = forms.CharField(label=_("Server name"))

    def handle(self, request, data):
        try:
            LOG.info('Creating server "%s"' % data['name'])
            new_server = api.moniker.server_update(request, data)
            messages.success(request, _('Server "%s" successfully created.' % data['name']))
        except:
            exceptions.handle(request, "Unable to create server")
        return True

################################################################################
# Domain forms

class AdminCreateDomainForm(forms.SelfHandlingForm):
    name  = forms.CharField(label=_("Domain name"))
    admin = forms.EmailField(label=_("Admin Email"))
    ttl   = forms.IntegerField(min_value=1, label=_("TTL (sec)"))

    def handle(self, request, data):
        try:
            LOG.info('Creating domain "%s"' % data['name'])
            new_domain = api.moniker.domain_create(request, data)
            messages.success(request, _('Domain "%s" successfully created.' % data['name']))
        except:
            exceptions.handle(request, "Unable to create domain")
        return True

class AdminUpdateDomainForm(forms.SelfHandlingForm):
    id    = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    name  = forms.CharField(label=_("Domain name"))
    admin = forms.EmailField(label=_("Admin Email"))
    ttl   = forms.IntegerField(min_value=1, label=_("TTL (sec)"))

    def handle(self, request, data):
        try:
            LOG.info('Updating domain "%s"' % data['name'])
            new_domain = api.moniker.domain_update(request, data)
            messages.success(request, _('Domain "%s" successfully updated.' % data['name']))
        except:
            exceptions.handle(request, "Unable to update domain")
        return True

################################################################################
# Record forms
#class AdminRecordForm(forms.SelfHandlingForm):
class AdminRecordForm(forms.SelfHandlingForm):
    RECORD_TYPES = ( ('', ''),
                     ('a', 'A'),
                     ('mx', 'MX'),
                     ('ns', 'NS'),
                     ('cname', 'CNAME'),
                     ('txt', 'TXT'),
                     )
    contributes = ("rec_type",
                   "priority",)

    id        = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    domain_id = forms.CharField(label=_("ID"), widget=forms.HiddenInput)
    rec_type  = forms.ChoiceField(label=_('Record type'),
                                required=True,
                                choices=RECORD_TYPES,
                                #widget=forms.Select(attrs={'class': 'switchable'}),
                                )

    name      = forms.CharField(label=_("Name"),
                                required=True)
    data      = forms.CharField(label=_("Data"),
                                required=True)
    priority  = forms.IntegerField(label=_("Priority"),
                                   min_value=0,
                                   required=True)
    ttl       = forms.IntegerField(label=_("TTL"),
                                   min_value=1,
                                   required=True)

    # def __init__(self,*args, **kwargs):
    #     print ("__init__")
    #     super(AdminRecordForm, self).__init__(*args, **kwargs)


    # def clean(self):
    #     print ("CLEAN")
    #     super(AdminRecordForm, self).clean()
    #     #cleaned_data = super(VolumeOptionsAction, self).clean()
    #     #record_opt = cleaned_data.get('rec_type', None)
    #     #if record_opt and not(cleaned_data[record_opt]):

    # def validate(self, value):
    #     print ("validate")
    #     super(AdminRecordForm, self).validate(value)

    # def clean_rec_type(self):
    #     print ("clean_rec_type")
    #     return self.cleaned_data


    # #def populate_priority_choices(self, request, context):
    # #    return [1,2,3,4,5,6]
    # def contribute(self, data, context):
    #     print "[AdminRecordForm::contribute]"
    #     context = super(AdminRecordForm, self).contribute(data, context)
    #     # Translate form input to context for volume values.
    #     if "rec_type" in data and data["rec_type"]:
    #         context['rec_type'] = data.get(data['rec_type'], None)

    #     if not context.get("rec_type", ""):
    #         context['rec_type'] = self.action.VOLUME_CHOICES[0][0]
    #         context['name'] = None
    #         context['data'] = None
    #         context['priority'] = None
    #         context['ttl'] = None
    #     return context



class AdminCreateRecordForm(AdminRecordForm):
    def handle(self, request, data):
        print "[AdminCreateRecordForm::handle]"
        try:
            print "CREATE RECORD"
            LOG.info('Creating record data:"%s", request:%s' % (data,request, ))
            new_domain = api.moniker.record_create(request, data)
            messages.success(request, _('Record "%s" successfully created.' % data['name']))
        except:
            exceptions.handle(request, "Unable to create record")
        return True


class AdminUpdateRecordForm(AdminRecordForm):
    def handle(self, request, data):
        print "[AdminUpdateRecordForm::handle]"
        try:
            LOG.info('Update record.  data:"%s", request:%s' % (data,request, ))
            new_domain = api.moniker.record_update(request, data)
            messages.success(request, _('Record "%s" successfully updated.' % data['name']))
        except:
            exceptions.handle(request, "Unable to update domain")
        return True

