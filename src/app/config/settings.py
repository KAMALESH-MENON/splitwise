import os

from dotenv import load_dotenv
 
def get_settings():

    local_env_path = "../.env"
 
    # Ensure the .env file is loaded

    if not os.path.exists(local_env_path):

        raise FileNotFoundError(f"Environment file not found: {local_env_path}")
 
    # Load environment variables

    load_dotenv(local_env_path, override=True)  # Forces loading from .env
 
    # Return the environment variables

    return {key: os.getenv(key) for key in os.environ.keys()}
 
# Load the config

app_config = get_settings()
 
# Print a specific env variable (for testing)

print(app_config)  # Check if env variables are loaded correctly

 