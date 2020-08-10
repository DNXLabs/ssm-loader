
import pytest
import os
import json
import boto3
from click.testing import CliRunner
from moto import mock_ssm


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(scope='function')
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ['AWS_ACCESS_KEY_ID'] = 'test'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'test'
    os.environ['AWS_SECURITY_TOKEN'] = 'test'
    os.environ['AWS_SESSION_TOKEN'] = 'test'


@pytest.fixture(scope='function')
def ssm(aws_credentials):
    with mock_ssm():
        yield boto3.client('ssm', region_name='us-east-1')


@pytest.fixture
def ssm_put_parameter(ssm):
    ssm.put_parameter(
        Name='/app/env/ssm_string',
        Description='description',
        Value='PLACEHOLDER',
        Type='String'
    )

    ssm.put_parameter(
        Name='/app/env/ssm_secure_string',
        Description='description secure string',
        Value='PLACEHOLDER',
        Type='SecureString'
    )


@pytest.fixture
def ssm_empty_parameters():
    result = {
        "parameters": []
    }
    return json.dumps(result, indent=4, sort_keys=True, default=str) + '\n'


@pytest.fixture
def load_command_parameters_output():
    return '/app/env/ssm_string OK\n/app/env/ssm_secure_string OK\n'


@pytest.fixture
def ssm_parameters():
    result = {
        "parameters": [
            {
                "Name": "/app/env/ssm_string",
                "Type": "String",
                "Value": "PLACEHOLDER",
                "Version": 1
            },
            {
                "Name": "/app/env/ssm_secure_string",
                "Type": "SecureString",
                "Value": "PLACEHOLDER",
                "Version": 1
            }
        ]
    }
    return json.dumps(result, indent=4, sort_keys=True, default=str) + '\n'
