from moto import mock_aws
import pytest
import boto3


@pytest.fixture
def mock_aws_credentials(monkeypatch):
    """Mocked AWS Credentials for moto."""
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "fake_access_key")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "fake_secret_key")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "fake_session_token")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")


@pytest.fixture
def config_bucket() -> str:
    return "test_config_bucket"


@pytest.fixture
def env_prefix() -> str:
    return "TEST_ENV_PREFIX"


@pytest.fixture
def mock_environment(monkeypatch, config_bucket, env_prefix) -> None:
    monkeypatch.setenv("CONFIG_BUCKET", config_bucket)
    monkeypatch.setenv("SPM_ENV", env_prefix)


@pytest.fixture
def main_config() -> str:
    return """main_setting_one: whatever1
main_setting_two: whatever2"""


@pytest.fixture
def table_config() -> str:
    return """tables:
    table1:
        table_setting_one: table_one_whatever
        table_setting_two: table_two_whatever
    table2:
        table_setting_one: table_two_whatever
        table_setting_two: table_two_whatever"""


@pytest.fixture
def s3_setup(mock_aws_credentials, config_bucket, env_prefix, main_config, table_config):
    with mock_aws():
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=config_bucket)

        s3_client.put_object(Bucket=config_bucket, Key=f'{env_prefix}/main.yaml', Body=main_config)
        s3_client.put_object(Bucket=config_bucket, Key=f'{env_prefix}/tables.yaml', Body=table_config)

        yield s3_client


def test_main(mock_environment, s3_setup):
    from src.main import main
    main()
