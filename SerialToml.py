import toml

with open("configuration.toml","r") as f:
    config = toml.load(f)

database_name = config["database"]["name"]
port = config["database"]["port"]
addr = config["database"]["addr"]
database_username = config["database"]["username"]
database_password = config["database"]["password"]
