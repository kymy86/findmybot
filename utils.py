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
    if os.environ['IS_LAMBDA'] == "1":
        return boto3.client('kms').decrypt(
            CiphertextBlob=b64decode(variable))['Plaintext']
    else:
        return variable
