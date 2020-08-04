from moto import mock_ssm
from ssm.cli import load
from tests.fixtures import aws_credentials, ssm, ssm_put_parameter, runner
from tests.fixtures import ssm_parameters, ssm_empty_parameters, load_command_parameters_output


def test_load_output_without_params(runner, ssm, ssm_empty_parameters):
    with runner.isolated_filesystem():
        with open('.env.ssm.json', 'w') as outfile:
            outfile.write(ssm_empty_parameters)
            outfile.close()

        result = runner.invoke(load)

        assert result.exit_code == 0
        assert result.output == ''


def test_load_output_with_params(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('.env.ssm.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load)

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output


def test_load_with_long_option_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('file.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load, ['--file', 'file.json'])

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output


def test_dump_with_short_option_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('file.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load, ['-f', 'file.json'])

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output


def test_dump_with_wrong_default_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('.env.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()

        result = runner.invoke(load)

        assert result.exit_code == 1
        assert result.output == 'No such file named .env.ssm.json in directory.\n'


def test_load_with_output_file_wront_termination(runner, ssm):
    result = runner.invoke(load, ['--file', 'file'])

    assert result.exit_code == 1
    assert result.output == 'Output file must ends with .json\n'
