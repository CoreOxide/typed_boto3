from pydantic import AnyHttpUrl, BaseModel, ConfigDict, SecretStr
from botocore.config import Config as BotocoreConfig

from typed_boto3._region import Region


class AwsCredentials(BaseModel):
    access_key_id: str
    secret_access_key: SecretStr
    session_token: SecretStr | None = None
    account_id: str | None = None


class ClientConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    region: Region | None = None
    credentials: AwsCredentials | None = None
    endpoint_url: AnyHttpUrl | None = None
    api_version: str | None = None
    use_ssl: bool = True
    verify: bool | str | None = None
    botocore_config: BotocoreConfig | None = None

    def to_boto_kwargs(self) -> dict[str, object]:
        out: dict[str, object] = {"use_ssl": self.use_ssl}
        if self.region is not None:
            out["region_name"] = self.region.value
        if self.endpoint_url is not None:
            out["endpoint_url"] = str(self.endpoint_url)
        if self.api_version is not None:
            out["api_version"] = self.api_version
        if self.verify is not None:
            out["verify"] = self.verify
        if self.credentials is not None:
            out["aws_access_key_id"] = self.credentials.access_key_id
            out["aws_secret_access_key"] = self.credentials.secret_access_key.get_secret_value()
            if self.credentials.session_token is not None:
                out["aws_session_token"] = self.credentials.session_token.get_secret_value()
            if self.credentials.account_id is not None:
                out["aws_account_id"] = self.credentials.account_id
        if self.botocore_config is not None:
            out["config"] = self.botocore_config
        return out
