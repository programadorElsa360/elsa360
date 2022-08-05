from dotenv import load_dotenv
from os import environ
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def get_env_variable(var_name, stage="development"):
    """Get the environment variable or return exception."""

    path = Path.cwd().resolve() / f".env.{stage}"
    load_dotenv(path)
    try:
        return environ[var_name]
    except KeyError:
        error_msg = f"Set the {var_name} environment variable"
        raise ImproperlyConfigured(error_msg)
