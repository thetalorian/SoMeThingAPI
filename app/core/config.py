from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    app_name: str = "SoMeThing API"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "test.db"

    @property
    def db_url(self) -> str:
        return f"sqlite:///{self.db_name}"


config = Config()