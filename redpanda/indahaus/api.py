# -*- coding: utf-8 -*-

"""API views."""

import json

import requests
import urllib3
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse_lazy
from djimix.decorators.auth import portal_auth_required
from redpanda.indahaus.manager import Client
from redpanda.packetfence.settings.local import API_EARL
from redpanda.packetfence.utils.helpers import get_token as get_token_nac
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@portal_auth_required(
    session_var='REDPANDA_INDAHAUS_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def spa(request):
    """Display all clients for all domain controllers for SPA."""
    client = Client()
    domains = settings.INDAHAUS_RF_DOMAINS
    token = client.get_token()
    for idx, domain in enumerate(domains):
        headers = {
            'accept': 'application/json',
            'Authorization': get_token_nac(),
        }
        devices = client.get_devices(domain['id'], token)
        pids = []
        if devices:
            # auth token from NAC
            for device_wap in devices:
                ap = device_wap['ap']
                mac = device_wap['mac'].replace('-', ':')
                url = '{0}{1}/{2}'.format(
                    API_EARL, settings.PACKETFENCE_NODE_ENDPOINT, mac,
                )
                response = requests.get(
                    url=url, headers=headers, verify=False,
                )
                device_nac = response.json()

                for key, _ in device_nac['item'].items():
                    if key == 'pid':
                        pid = device_nac['item'][key].lower()
                        # some folks are registered with their username
                        # and their email address for some reason.
                        if '@{0}'.format(settings.LDAP_EMAIL_DOMAIN) in pid:
                            pid = pid.split('@')[0]
                        status = (
                            pid not in settings.INDAHAUS_XCLUDE and
                            'host/' not in pid and
                            'carthage\\' not in pid
                        )
                        if status:
                            if pid not in pids:
                                pids.append(pid)
                            # check for areas within a domain
                            if domains[idx]['areas']:
                                for area in domains[idx]['areas']:
                                    if ap in area['aps']:
                                        if pid not in area['pids']:
                                            area['pids'].append(pid)
                            else:
                                domains[idx]['areas'] = None
            # update RF domain with the total number of pids
            domains[idx]['pids'] = len(pids)
            domains[idx]['capacity'] = round(
                domains[idx]['pids'] / domains[idx]['capacity'] * 100,
            )
            # update areas with total number of pids
            if domains[idx]['areas']:
                for aid, _ in enumerate(domains[idx]['areas']):
                    count = len(domains[idx]['areas'][aid]['pids'])
                    domains[idx]['areas'][aid]['pids'] = count
                    cap = domains[idx]['areas'][aid]['capacity']
                    domains[idx]['areas'][aid]['capacity'] = round(
                        count / cap * 100,
                    )

    # destroy the authentication token
    client.destroy_token(token)

    return HttpResponse(
        json.dumps(domains), content_type='text/plain; charset=utf-8',
    )


@portal_auth_required(
    session_var='REDPANDA_INDAHAUS_AUTH',
    redirect_url=reverse_lazy('access_denied'),
)
def clients(request, domain):
    """Display all clients given a domain controller identifier."""
    client = Client()
    token = client.get_token()
    devices = client.get_devices(domain, token)
    pids = []
    if devices:
        # auth token from NAC
        headers = {
            'accept': 'application/json', 'Authorization': get_token_nac(),
        }
        for device_wap in devices:
            mac = device_wap['mac'].replace('-', ':')
            url = '{0}{1}/{2}'.format(
                API_EARL, settings.PACKETFENCE_NODE_ENDPOINT, mac,
            )
            response = requests.get(url=url, headers=headers, verify=False)
            device_nac = response.json()

            for key, _ in device_nac['item'].items():
                if key == 'pid':
                    pid = device_nac['item'][key].lower()
                    if pid not in pids:
                        pids.append(pid)

    # sign out
    client.destroy_token(token)
    jason = json.dumps({'pids': pids, 'count': len(pids)})
    return HttpResponse(jason, content_type='text/plain; charset=utf-8')
