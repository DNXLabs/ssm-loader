from moto import mock_ssm
from ssm.cli import dump
from tests.fixtures import aws_credentials, ssm, ssm_put_parameter, runner
from tests.fixtures import ssm_parameters, ssm_empty_parameters


def test_dump_output_without_params(runner, ssm, ssm_empty_parameters):
    with runner.isolated_filesystem():
        result = runner.invoke(dump, ['/app/env/ssm'])

        assert result.exit_code == 0
        assert result.output == ssm_empty_parameters


def test_dump_output_with_params(runner, ssm, ssm_put_parameter, ssm_parameters):
    with runner.isolated_filesystem():
        result = runner.invoke(dump, ['/app/env'])

        assert result.exit_code == 0
        assert result.output == ssm_parameters


def test_dump_with_long_option_output_file(runner, ssm, ssm_put_parameter):
    with runner.isolated_filesystem():
        result = runner.invoke(dump, ['--output', 'file.json', '/app/env'])

        outfile = open('file.json', 'r')

        assert result.exit_code == 0
        assert result.output == outfile.read() + '\n'


def test_dump_with_short_option_output_file(runner, ssm, ssm_put_parameter):
    with runner.isolated_filesystem():
        result = runner.invoke(dump, ['-o', 'file.json', '/app/env'])

        outfile = open('file.json', 'r')

        assert result.exit_code == 0
        assert result.output == outfile.read() + '\n'


def test_dump_with_default_output_file(runner, ssm, ssm_put_parameter):
    with runner.isolated_filesystem():
        result = runner.invoke(dump, ['/app/env'])

        outfile = open('.env.ssm.json', 'r')

        assert result.exit_code == 0
        assert result.output == outfile.read() + '\n'


def test_dump_with_output_file_wront_termination(runner, ssm):
    result = runner.invoke(dump, ['--output', 'file', '/app/env'])

    assert result.exit_code == 1
    assert result.output == 'Output file must ends with .json\n'
