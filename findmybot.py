
import os
import re
from lxml import html
import requests
import json
import boto3
from url_getter import UrlsGetter
from mcutils import build_message

def is_the_original_invokation(event):
    return False if 'domains' in event else True

def lambda_handler(event, context):
    """
    Call the main function
    """
    print(event)
    # check if it's the original invokation or not.
    if is_the_original_invokation(event):
        # original invocation. Go on as usual
        ugetter = UrlsGetter()
        domains = ugetter.get_domains_list()
        domains_wn_meta = []
        sub = False
    else:
        # Sub invokation. Resume the info from the context
        domains = event['domains']
        domains_wn_meta = event['domains_wn_meta']
        sub = True

    for domain in domains:
        try:
            page = requests.get('http://'+domain, allow_redirects=False, timeout=20)
            if page.status_code == 200:
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
        domains.remove(domain)

        print(context.get_remaining_time_in_millis())
        if context.get_remaining_time_in_millis() <= 40000:
            client = boto3.client('lambda')
            client.invoke(
                FunctionName=context.function_name,
                InvocationType='Event',
                Payload=json.dumps({
                    'domains':domains,
                    'domains_wn_meta':domains_wn_meta
                })
            )
            sub = True
            break
        else:
            sub = False

    if sub is True:
        return 1
    else:
        if len(domains_wn_meta) != 0:
            message = build_message(domains_wn_meta)
            sns = boto3.client('sns')
            response = sns.publish(TopicArn=os.environ['TOPIC_ARN'],
                                Message=message,
                                Subject="Meta Robots: weekly status")
            return response['MessageId']


if __name__ == '__main__':
    lambda_handler(event=None, context=None)
