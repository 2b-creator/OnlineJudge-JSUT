from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def index():
    return "hello world"


@app.route('/api/submit', methods=['POST'])
def submit_code():
    questions_id = request.values.get("id")


if __name__ == "__main__":
    app.run()
