from flask import Flask, request, jsonify
from flask_script import Manager
from analyzer import get_problems, Comment
from finalizing import grade as f_grade

app = Flask(__name__)
manager = Manager(app)

HTTPEXCEPTIONS = {
    1:"BAD REQUEST:No 'code' field",
    2:"BAD REQUEST:Code Execution Error",
    3: "BAD REQUEST:No 'comment' field"
}

def illegal_request(id):
    return HTTPEXCEPTIONS.get(id),400

@app.route('/get_comment/', methods=['POST'])
def get_comment():
    if "code" not in request.json:
        return illegal_request(1)
    code = request.json.get("code")
    result = get_problems(code)
    return jsonify(result)

@app.route('/grade/', methods=['POST'])
def grade():
    if "comment" not in request.json:
        return illegal_request(3)
    comment = request.json.get("comment")
    result = f_grade(comment)
    return jsonify(result)

if __name__ == "__main__":
    manager.run()
