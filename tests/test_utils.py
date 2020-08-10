from moto import mock_ssm
from ssm.utils import print_error_ssm_load, print_ok_ssm_load


def test_print_ok():
    result = print_ok_ssm_load(parameter_name='param')

    assert result == 'param\x1b[32m OK\x1b[0m'


def test_print_ok_empty():
    result = print_ok_ssm_load(parameter_name='')

    assert result == '\x1b[32m OK\x1b[0m'


def test_print_error():
    result = print_error_ssm_load(parameter_name='param')

    assert result == 'param\x1b[31m FAIL\x1b[0m'

def test_print_error_empty():
    result = print_error_ssm_load(parameter_name='')

    assert result == '\x1b[31m FAIL\x1b[0m'
