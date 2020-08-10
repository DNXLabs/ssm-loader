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

        response = ssm.get_parameters(Names=['/app/env/ssm_string', '/app/env/ssm_secure_string'])
        assert len(response["Parameters"]) == 0


def test_load_output_with_params(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('.env.ssm.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load)

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output

        response = ssm.get_parameters(Names=['/app/env/ssm_string', '/app/env/ssm_secure_string'])
        assert len(response["Parameters"]) == 2

        assert response["Parameters"][0]['Name'] == '/app/env/ssm_string'
        assert response["Parameters"][0]['Type'] == 'String'
        assert response["Parameters"][0]['Value'] == 'PLACEHOLDER'

        assert response["Parameters"][1]['Name'] == '/app/env/ssm_secure_string'
        assert response["Parameters"][1]['Type'] == 'SecureString'
        assert response["Parameters"][1]['Value'] == 'kms:default:PLACEHOLDER'


def test_load_with_long_option_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('file.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load, ['--file', 'file.json'])

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output

        response = ssm.get_parameters(Names=['/app/env/ssm_string', '/app/env/ssm_secure_string'])
        assert len(response["Parameters"]) == 2

        assert response["Parameters"][0]['Name'] == '/app/env/ssm_string'
        assert response["Parameters"][0]['Type'] == 'String'
        assert response["Parameters"][0]['Value'] == 'PLACEHOLDER'

        assert response["Parameters"][1]['Name'] == '/app/env/ssm_secure_string'
        assert response["Parameters"][1]['Type'] == 'SecureString'
        assert response["Parameters"][1]['Value'] == 'kms:default:PLACEHOLDER'


def test_dump_with_short_option_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('file.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()
        result = runner.invoke(load, ['-f', 'file.json'])

        assert result.exit_code == 0
        assert result.output == load_command_parameters_output

        response = ssm.get_parameters(Names=['/app/env/ssm_string', '/app/env/ssm_secure_string'])
        assert len(response["Parameters"]) == 2

        assert response["Parameters"][0]['Name'] == '/app/env/ssm_string'
        assert response["Parameters"][0]['Type'] == 'String'
        assert response["Parameters"][0]['Value'] == 'PLACEHOLDER'

        assert response["Parameters"][1]['Name'] == '/app/env/ssm_secure_string'
        assert response["Parameters"][1]['Type'] == 'SecureString'
        assert response["Parameters"][1]['Value'] == 'kms:default:PLACEHOLDER'



def test_dump_with_wrong_default_input_file(runner, ssm, ssm_parameters, load_command_parameters_output):
    with runner.isolated_filesystem():
        with open('.env.json', 'w') as outfile:
            outfile.write(ssm_parameters)
            outfile.close()

        result = runner.invoke(load)

        assert result.exit_code == 1
        assert result.output == 'No such file named .env.ssm.json in directory.\n'

        response = ssm.get_parameters(Names=['/app/env/ssm_string', '/app/env/ssm_secure_string'])
        assert len(response["Parameters"]) == 0


def test_load_with_output_file_wront_termination(runner, ssm):
    result = runner.invoke(load, ['--file', 'file'])

    assert result.exit_code == 1
    assert result.output == 'Output file must ends with .json\n'
