"""Application configuration module."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration."""

    DEBUG = False
    TESTING = False
    VALID_API_KEYS = os.getenv(
        "VALID_API_KEYS", "default-key-1,default-key-2"
    ).split(",")


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    VALID_API_KEYS = ["test-key-1", "test-key-2"]


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
