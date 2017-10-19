"""
Return a list of domains available on a
CPanel staging server
"""
import os
import re
import json
import requests
from mcutils import get_env


class UrlsGetter():
    """
    Perform the connection to the WHM
    and get the list of domains currently
    available on it.
    """
    def __init__(self):
        self._url = os.environ['WHM_URL']+"/json-api/listaccts?api.version=1&want=domain,suspended"
        self._user = get_env(os.environ['WHM_USER'])
        self._auth = get_env(os.environ['WHM_TOKEN'])

    def __connect(self):
        pattern = re.compile(r'(\r|\n)')
        headers = {
            'Authorization':'WHM {user}:{hash}'.format(
                user=self._user,
                hash=pattern.sub("", self._auth)
            )
        }
        try:
            r = requests.get(self._url, headers=headers, allow_redirects=False, timeout=10)
            return r
        except requests.RequestException:
            print("A connection error has occured")

    def get_domains_list(self):
        """
        Return a list of domains
        """
        response = self.__connect()
        domains = response.text
        domainsj = json.loads(domains)
        cp_domains = []
        for domain in domainsj['data']['acct']:
            if domain['domain'] != 'rstplan.temp':
                if domain['suspended'] == 0:
                    cp_domains.append(domain['domain'])
        return cp_domains