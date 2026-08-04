import os
from kaggle.api.kaggle_api_extended import KaggleApi

print("KAGGLE_API_TOKEN:", os.getenv("KAGGLE_API_TOKEN"))
api = KaggleApi()
api.authenticate()                # will raise if the token is invalid
print("Authenticated as:", api.get_config_value("username"))
