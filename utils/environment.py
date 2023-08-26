import os

def get_name_suffix():
    environment = os.environ.get("ENV")

    if environment == "dev":
        return "dev"
    elif environment == "main":
        return "main"
    elif environment == "test":
        return "test"
    else:
        raise ValueError("Unknown environment: {}".format(environment))
