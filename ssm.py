#!/usr/bin/env python3
import boto3
import click
import os
import fileinput
import configparser
from pprint import pprint
import json


class bcolors:
    OK = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


ssm_client = boto3.client("ssm", region_name=os.environ.get('AWS_REGION', 'us-east-1'))


@click.group()
def cli():
    """A CLI wrapper for the SSM."""


@cli.command()
@click.argument('path')
@click.option('-o', '--output', default='.env.ssm.json', help='Name to the output JSON file.')
def dump(path: str, output: str):
    """Get all cataloged credentials and save it on a file."""
    next_token = ''
    parameters = []
    extra_args = {
        'Path': path,
        'Recursive':False,
        'WithDecryption': True,
        'MaxResults': 2
    }
    data = {}

    while True:
        response = ssm_client.get_parameters_by_path(**extra_args)
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            exit(1)

        parameters = parameters + response['Parameters']

        if not 'NextToken' in response:
            break

        extra_args['NextToken'] = response['NextToken']

    data['parameters'] = parameters

    print(json.dumps(data, indent=4, sort_keys=True, default=str))

    with open(output, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True, default=str)


@click.option('-f', '--file', default='.env.ssm.json', help='Name to the JSON file.')
@cli.command()
def load(file: str):
    """Load all cataloged credentials from a file and update the SSM client."""
    with open(file) as json_file:
        data = json.load(json_file)
        for param in data['parameters']:
            args = {
                'Name': param['Name'],
                'Value': param['Value'],
                'Overwrite': True,
                'Type': "String",
                'Tier': "Intelligent-Tiering"
            }
            response = ssm_client.put_parameter(**args)
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                print(param['Name'] + bcolors.FAIL + ' FAIL' + bcolors.ENDC)
                exit(1)
            else:
                print(param['Name'] + bcolors.OK + ' OK' + bcolors.ENDC)