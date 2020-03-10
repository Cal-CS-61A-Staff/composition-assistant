from flask import Flask, request, jsonify
from flask_script import Manager
from analyzer import get_problems, Comment, PROBLEMS,check_problem
from finalizing import grade as f_grade
from ok_interface import get_backup_ids as f_get_backup_ids, submit_comment
import requests
import auth
from ok_interface import ACCESS_TOKEN

app = Flask(__name__)
manager = Manager(app)

HTTPEXCEPTIONS = {
    1:"BAD REQUEST:No 'code' field",
    2:"BAD REQUEST:Code Execution Error",
    3: "BAD REQUEST:No 'comment' field",
    4:"BAD REQUEST: Illegal Files"
}

def illegal_request(id):
    return HTTPEXCEPTIONS.get(id),400

@app.route('/api/get_backup_ids', methods=['GET'])
def get_backup_ids():
    id = request.args.get('id',default = -1, type = int)
    print ("THIS is: ",id)
    return "x"

@app.route('/api/get_backup_problems', methods=['GET'])
def get_backup_problems():
    id = request.args.get('id', default="", type=str)
    print ("THIS is: ", id)
    params = {"access_token": ACCESS_TOKEN}
    r = requests.get(f"https://okpy.org/api/v3/backups/{id}", params=params)
    messages = r.json()["data"]["messages"][0]
    out = []
    print("MESSEGSES:", messages)
    for proj_name in PROBLEMS:
        print(proj_name+".py")
        if proj_name+".py" in messages["contents"]:
            problems = PROBLEMS[proj_name]
            project = proj_name
            code =  messages["contents"][proj_name+".py"]
            break
    else:
        return illegal_request(4)
    for name, (start, end) in problems.items():
        start_index = code.index(start)
        end_index = code.index(end)
        initial_line_number = code[:start_index].count("\n") + 1
        func_code = code[start_index:end_index].strip()
        out.append({"problem_name":name,"problem_body":func_code,"initial_line_number":initial_line_number})

    return jsonify(out)

@app.route('/get_potential_comments', methods=['POST'])
def get_comment():
    try:
        code = request.json.get("problem_body")
        problem = request.json.get("problem_name")
        init_line = request.json.get("initial_line_number")
    except:
        return illegal_request(1)
    result = check_problem(code,problem,init_line)
    return jsonify(result)

@app.route('/submit_comment/', methods=['POST'])
def grade():
    try:
        id = request.json.get("id")
        comments = request.json.get("comments")
    except:
        return illegal_request(3)
    result = f_grade(comments)
    for comment in comments:
        submit_comment(id,comment["line_num"],comment["comment"])
    return jsonify(result)


if __name__ == "__main__":
    manager.run()
