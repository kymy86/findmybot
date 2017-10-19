
import os
import re
from lxml import html
import requests
import boto3
from url_getter import UrlsGetter
from mcutils import build_message


def lambda_handler(event, context):
    """
    Call main function
    """
    ugetter = UrlsGetter()
    domains = ugetter.get_domains_list()
    domains_wn_meta = []

    for domain in domains:
        try:
            page = requests.get('http://'+domain, allow_redirects=False, timeout=20)
            if page.status_code == 200:
                print("http://"+domain)
                tree = html.fromstring(page.content)
                h1 = tree.xpath('//title/text()')
                title = h1[0] if len(h1) > 0 else ""
                if title != 'Index of /':
                    meta = tree.xpath('//meta[re:test(@name, "^robots$", "i")]/@content',
                                      namespaces={"re": "http://exslt.org/regular-expressions"})
                    if len(meta) == 0:
                        domains_wn_meta.append(domain)
                    elif re.match('noindex', ",".join(meta), re.IGNORECASE) is None:
                        domains_wn_meta.append(domain)
        except Exception as e:
            print(e)

    if len(domains_wn_meta) != 0:
        message = build_message(domains_wn_meta)
        sns = boto3.client('sns')
        response = sns.publish(TopicArn=os.environ['TOPIC_ARN'],
                               Message=message,
                               Subject="Meta Robots: weekly status")
        return response['MessageId']


if __name__ == '__main__':
    lambda_handler(event=None, context=None)
