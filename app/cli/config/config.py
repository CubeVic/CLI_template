
from functools import lru_cache
import os
from pathlib import Path

from dotenv import load_dotenv
import tomllib
from typing import Optional
from pydantic import BaseModel, Field, SecretStr


CONFIG_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENV_PATH = CONFIG_DIR / ".env"
CONFIG_PATH = CONFIG_DIR / "config.toml"

load_dotenv(dotenv_path=ENV_PATH)


def _mask_if_secret(key: str, value: str):
    key_lower = key.lower()
    if any(s in key_lower for s in ("key", "token", "secret", "password")):
        return SecretStr(value)
    return value


class AppConfig(BaseModel):
    app_name: str = Field(..., description="Name of the application")
    app_version: str = Field(..., description="Version of the application")


class LoggingConfig(BaseModel):
    level: str = Field("INFO", description="Logging level")
    format: str = Field("%(asctime)s - %(name)s - %(levelname)s - %(message)s", description="Logging format")
    use_rich: bool = Field(True, description="Use rich for logging")


class FeatureConfig(BaseModel):
    greetings: str = Field("Hello", description="Greeting message")
    env_prefix: str = Field("APP_", description="Prefix for environment variables")


# this can use BaseSettings from pydantic_settings but couln't get it to work when the env_prefix is set in the toml
# I couldn't maked it work as a "dynamically" load the prefix and then build the env model using Base Settings.
class EnvConfig(BaseModel):
    env: str = Field("development", description="Environment of the application")
    secret_key: Optional[SecretStr] = Field(None, description="Secret key for the application")


class Config(BaseModel):
    app: AppConfig
    logging: LoggingConfig
    features: FeatureConfig
    env: EnvConfig = Field(default_factory=EnvConfig)

    @classmethod
    def load(cls) -> "Config":
        config_dict = {}

        # Step 1: Load from config.toml
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "rb") as f:
                config_dict = tomllib.load(f)

        # build the env object so the model can be later build
        env_config = {}
        # make sure to extract only env variable swith the prefix set in the toml if not use `APP_`
        env_prefix = config_dict.get("features", {}).get("env_prefix", "APP_")

        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                env_key = key[len(env_prefix):].lower()
                env_config[env_key] = _mask_if_secret(key, value)

        config_dict["env"] = env_config

        return cls.model_validate(config_dict)


@lru_cache()
def get_config() -> Config:
    return Config.load()
