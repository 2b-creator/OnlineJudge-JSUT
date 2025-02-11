import toml

with open("configuration.toml","r") as f:
    config = toml.load(f)

database_name = config["database"]["name"]
port = config["database"]["port"]
addr = config["database"]["addr"]
database_username = config["database"]["username"]
database_password = config["database"]["password"]

root_stu_id = config["root"]["stu_id"]
root_username = config["root"]["username"]
root_nickname = config["root"]["nickname"]
root_password = config["root"]["password"]
root_role = "admin"
root_email = config["root"]["email"]

cp_cpu_limit = config["limit"]["complie_cpu"]
cp_mem_limit = config["limit"]["complie_memory"]
cp_time_limit = config["limit"]["complie_time"]
output_limit = config["limit"]["output_limit"]