from os import path

from dotenv.main import dotenv_values


def get_settings():
    """
    Load environment variables from a local .env file if it exists.

    Returns:
        dict: A dictionary containing key-value pairs from the .env file.
    """
    secrets = {}

    local_env_path = ".env"
    if path.exists(local_env_path):
        secrets.update(dotenv_values(local_env_path))
    return secrets


app_config = get_settings()
