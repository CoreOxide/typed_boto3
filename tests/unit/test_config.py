from botocore.config import Config as BotocoreConfig

from typed_boto3 import AwsCredentials, ClientConfig, Region


def test_to_boto_kwargs_minimal_defaults_use_ssl_true():
    out = ClientConfig().to_boto_kwargs()
    assert out == {"use_ssl": True}


def test_to_boto_kwargs_region_and_flags():
    out = ClientConfig(
        region=Region.EU_WEST_1,
        api_version="2012-11-05",
        use_ssl=False,
        verify=False,
    ).to_boto_kwargs()
    assert out["region_name"] == "eu-west-1"
    assert out["api_version"] == "2012-11-05"
    assert out["use_ssl"] is False
    assert out["verify"] is False


def test_to_boto_kwargs_endpoint_url_stringified():
    out = ClientConfig(endpoint_url="https://s3.example.internal").to_boto_kwargs()
    assert str(out["endpoint_url"]).startswith("https://s3.example.internal")


def test_to_boto_kwargs_credentials_unwraps_secrets():
    creds = AwsCredentials(
        access_key_id="AKIA",
        secret_access_key="shh",
        session_token="tok",
        account_id="111111111111",
    )
    out = ClientConfig(credentials=creds).to_boto_kwargs()
    assert out["aws_access_key_id"] == "AKIA"
    assert out["aws_secret_access_key"] == "shh"
    assert out["aws_session_token"] == "tok"
    assert out["aws_account_id"] == "111111111111"


def test_to_boto_kwargs_credentials_omit_optional_fields():
    creds = AwsCredentials(access_key_id="AKIA", secret_access_key="shh")
    out = ClientConfig(credentials=creds).to_boto_kwargs()
    assert "aws_session_token" not in out
    assert "aws_account_id" not in out


def test_to_boto_kwargs_passes_botocore_config_through():
    cfg = BotocoreConfig(retries={"max_attempts": 5})
    out = ClientConfig(botocore_config=cfg).to_boto_kwargs()
    assert out["config"] is cfg


def test_aws_credentials_repr_hides_secret():
    creds = AwsCredentials(access_key_id="AKIA", secret_access_key="supersecret")
    assert "supersecret" not in repr(creds)
