"""
Common utils
"""
import os
from base64 import b64decode
import boto3


def get_env(variable):
    """
    If is lambda environment, return the decrypting variable
    otherwise return it in plain text
    """
    if "SERVERTYPE" not in os.environ:
        env_variable = boto3.client('kms').decrypt(
            CiphertextBlob=b64decode(variable))['Plaintext']
        return env_variable.decode('utf-8')
    else:
        return variable

def build_message(valid_dm):
    """
    Build notification message
    """
    message = '''
    The following domains are setup on the staging environment without the meta tag robots noindex/nofollow.\n
    Action is required!\n\n'''
    for domain in valid_dm:
        message += "- "+domain+"\n"

    return message
