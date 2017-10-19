# Python lambda function

[![Build Status](https://travis-ci.org/kymy86/findmybot.svg?branch=master)](https://travis-ci.org/kymy86/findmybot)

This [Amazon Lambda] function grabs a list of domains from WHM manager and it checks one by one to discover if they have correctly set the meta tag robots with noindex/nofollow values. In the end, it sends an notification with AWS [SNS].

The Lambda function is deployed by using the [Zappa] Framework.
The default trigger for the function is a CloudWatch scheduled Event (every days from Mon to Fri at 0:00)

[Amazon Lambda]: https://aws.amazon.com/lambda/
[SNS]: https://aws.amazon.com/sns/ 
[remote source]: https://documentation.cpanel.net/display/SDK/Guide+to+WHM+API+1
[Zappa]: https://www.zappa.io/

## Getting started

1. Set up the following AWS Lambda environment variables:
    - WHM_URL: the WHM main url 
    - WHM_USER: the WHM username (must be encrypted with the KMS key)
    - WHM_TOKEN: the WHM token to access the CPanel from [remote source] (must be encrypted with the KMS key)
    - TOPIC_ARN: the SNS topic where send the message with the list of "invalid" domains.

2. Install the Zappa framework `pip install zappa`
3. Optional: configure the Zappa framework from the **zappa_settings.yml** file
4. Deploy the Lambda function with the command `zappa deploy run`

**N.B.** If you want to test the function on your local machine, set-up a *SERVERTYPE* environment variable, so that the the KMS encryption is not applied.