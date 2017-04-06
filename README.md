# Python lambda function

[![Build Status](https://travis-ci.org/kymy86/findmybot.svg?branch=master)](https://travis-ci.org/kymy86/findmybot)

This Python script grabs a list of domains from WHM manager and it checks one by one to discover if they have correctly set the meta tag robots with noindex/nofollow values. In the end, it sends an email with [SES] with the list of domains discovered.

This script is compatible with [Amazon Lambda] serverless application.

[Amazon Lambda]: https://aws.amazon.com/lambda/
[SES]: https://aws.amazon.com/ses/ 
[remote source]: https://documentation.cpanel.net/display/SDK/Guide+to+WHM+API+1

## Getting started

1. Set up the following environment variables:
    - WHM_URL: the WHM main url
    - WHM_USER: the WHM username
    - WHM_TOKEN: the WHM token to access the cpanel from [remote source]
    - FROM_ADDR: the email sender email address
    - TO_ADDR: the recipients email addresses
    - SES_REGION_NAME: the region name of the SES service
    - IS_LAMBDA: 1 if it's going to use with AWS Lambda, 0 otherwise.