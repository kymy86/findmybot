#pylint: disable=C0103

from __future__ import print_function
import os
from lxml import html
import requests
import boto3
from urls_getter import UrlsGetter

client = boto3.client('ses', region_name=os.environ['SES_REGION_NAME'])
ugetter = UrlsGetter()
domains = ugetter.getDomainList()
domains_wn_meta = []

def build_message(valid_dm):
    """
    Build email message
    """
    message = '''
    The following domains are setup on the staging environment without the meta tag
    robots noindex/nofollow.<br />
    <b>Action is required!</b><br /><br />
    <ul>
    '''

    for domain in valid_dm:
        message += "<li>"+domain+"</li>"
    message += "</ul>"

    body = {
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
    return body


def lambda_handler(event, context):
    """
    Call main function
    """
    for domain in domains:
        try:
            page = requests.get('http://'+domain, allow_redirects=False, timeout=5)
            tree = html.fromstring(page.content)
            h1 = tree.xpath('//title/text()')
            title = h1[0] if len(h1) > 0 else ""
            status_code = page.status_code
            meta = tree.xpath('//meta[@name="robots"]/@content')
            if status_code == 200 and title != 'Index of /':
                if len(meta) == 0:
                    domains_wn_meta.append(domain)
        except Exception as e:
            print(e)

    if len(domains_wn_meta) == 0:
        return {
            'message': 'No invalid domains found'
        }

    message = build_message(domains_wn_meta)

    email_to = os.environ['TO_ADDR']
    client.send_email(
        Source=os.environ['FROM_ADDR'],
        Destination={
            'ToAddresses':email_to.split(",")
        },
        Message=message
    )

    return {
        'message': "Ok, email sent!"
    }

if __name__ == '__main__':
    lambda_handler(event=None, context=None)
