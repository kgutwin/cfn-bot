import os
import boto3
import hashlib

dynamo = boto3.client('dynamodb')
TABLE_NAME = os.environ.get('TABLE_NAME')


def hash_atom(atom):
    m = hashlib.sha256()
    for k in atom:
        m.update(k.encode('utf-8'))
    return m.hexdigest()


def has_atom(atom):
    key = hash_atom(atom)
    item = dynamo.get_item(
        TableName=TABLE_NAME,
        Key={'hash': {'S': key}})
    return 'Item' in item


def save_atom(atom):
    key = hash_atom(atom)
    dynamo.put_item(
        TableName=TABLE_NAME,
        Item={
            'hash': {'S': key},
            'subject': {'S': atom[0]},
            'description': {'S': atom[1]},
            'link': {'S': repr(atom[2])},
            'date': {'S': atom[3]}
        }
    )
