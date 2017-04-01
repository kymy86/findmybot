#pylint: disable=C0103

from lxml import html
import requests
from classes.urls_getter import UrlsGetter

ugetter = UrlsGetter()
domains = ugetter.getDomainList()

for domain in domains:
    try:
        page = requests.get('http://'+domain)
        tree = html.fromstring(page.content)
        h1 = tree.xpath('//title/text()')
        title = h1[0]
        status_code = page.status_code
        meta = tree.xpath('//meta[@name="robots"]/@content')
        if status_code != 200 or title != 'Index of /':
            if len(meta) == 0:
                print("{domain} hasn't any meta".format(domain=domain))
    except Exception:
        pass

