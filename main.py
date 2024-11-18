from flask import Flask, request
from UserAdmin.UserLogic import *

app = Flask(__name__)

@app.route('/')
def index():
    return "hello world"


@app.route('/api/submit', methods=['POST'])
def submit_code():
    pass


if __name__ == "__main__":
    app.run()
