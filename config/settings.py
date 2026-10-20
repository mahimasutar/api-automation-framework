from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="config/.env")

    base_url: str = "https://restful-booker.herokuapp.com"
    request_timeout: float = 15.0
    rb_username: str
    rb_password: str


settings = Settings()
