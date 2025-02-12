import requests

with open("./Scripts/ShellScripts/submit.cpp") as f:
    strs = f.read()

dic = {"id": 1,
       "code": strs,
       "language": "cpp"}

print(dic)
