#pylint: disable=C0103

"""
Return a list of domains available on a
CPanel staging server
"""
import os
import re
import logging
import json
import requests
from utils import get_env


class UrlsGetter():
    """
    Perform the connection to the WHM
    and get the list of domains currently
    available on it.
    """
    def __init__(self):
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
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
            logging.error("A connection error has occured")

    def getDomainList(self):
        """
        Return a list of domains
        """
        response = self.__connect()
        domains = response.text
        domainsj = json.loads(domains)
        cpDomains = []
        for domain in domainsj['data']['acct']:
            if domain['suspended'] == 0:
                cpDomains.append(domain['domain'])
        return cpDomains



