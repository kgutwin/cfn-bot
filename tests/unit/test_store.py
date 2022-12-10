from moto import mock_dynamodb
import boto3
import pytest

from cfnbot import store


@pytest.fixture
def mock_dynamo_table(mocker):
    mock_dynamodb_instance = mock_dynamodb()
    mock_dynamodb_instance.start()
    boto3.setup_default_session()
    mocker.patch.object(store, 'dynamo', boto3.client('dynamodb'))
    mocker.patch.object(store, 'TABLE_NAME', 'moto_store')

    store.dynamo.create_table(
        TableName='moto_store',
        AttributeDefinitions=[{'AttributeName': 'hash', 'AttributeType': 'S'}],
        KeySchema=[{'AttributeName': 'hash', 'KeyType': 'HASH'}],
        ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
    )

    yield

    store.dynamo.delete_table(TableName='moto_store')


def test_has_atom(mock_dynamo_table):
    assert not store.has_atom(('foo', 'bar', 'http://baz', 'December 1, 2018'))


def test_save_atom(mock_dynamo_table):
    atom = ('foo', 'baz', 'http://baz', 'December 2, 2018')
    store.save_atom(atom)
    assert store.has_atom(atom)
