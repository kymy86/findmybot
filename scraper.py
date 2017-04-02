#pylint: disable=C0103

import os
import sys
from lxml import html
import requests
import boto3
from urls_getter import UrlsGetter

client = boto3.client('ses', region_name='us-east-1')

ugetter = UrlsGetter()
domains = ugetter.getDomainList()
domains_wn_meta = []


def lambda_handler(event, context):
    for domain in domains:
        try:
            page = requests.get('http://'+domain)
            tree = html.fromstring(page.content)
            h1 = tree.xpath('//title/text()')
            title = h1[0]
            status_code = page.status_code
            meta = tree.xpath('//meta[@name="robots"]/@content')
            if status_code == 200 and title != 'Index of /':
                if len(meta) == 0:
                    domains_wn_meta.append(domain)
        except Exception:
            pass

    if len(domains_wn_meta) == 0:
        sys.exit(1)

    message = '''
    The following domains are setup on the staging environment without the meta tag
    robots noindex/nofollow.<br />
    <b>Action is required!</b><br /><br />
    <ul>
    '''

    for domain in domains_wn_meta:
        message += "<li>"+domain+"</li>"
    message += "</ul>"

    email_to = os.environ['TO_ADDR']
    response = client.send_email(
        Source=os.environ['FROM_ADDR'],
        Destination={
            'ToAddresses':email_to.split(",")
        },
        Message={
            'Subject': {
                'Data': "Meta Robots: weekly status",
            },
            'Body': {
                'Html': {
                    'Data': message,
                },
                'Text': {
                    'Data': message
                }
            },
        }
    )
