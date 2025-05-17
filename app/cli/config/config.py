
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


class EnvConfig(BaseModel):
    app_env: str = Field("development", description="Environment of the application")
    app_secret_key: Optional[SecretStr] = Field(None, description="Secret key for the application")


class Config(BaseModel):
    app: AppConfig
    logging: LoggingConfig
    features: FeatureConfig
    env: EnvConfig = Field(default_factory=EnvConfig)

    @classmethod
    def load(cls):
        config = {}
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "rb") as f:
                config = tomllib.load(f)

        # Build the 'env' section explicitly
        env_section = {}
        for k, v in os.environ.items():
            k_lower = k.lower()

            # Map to expected nested keys
            if k_lower == "app_env":
                env_section["app_env"] = v
            elif k_lower == "app_secret_key":
                env_section["app_secret_key"] = _mask_if_secret(k, v)

        # Merge into config under 'env'
        config["env"] = env_section

        return cls.model_validate(config)


@lru_cache()
def get_config() -> Config:
    return Config.load()