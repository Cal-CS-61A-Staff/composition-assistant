import re
import webbrowser

import requests

import auth

ACCESS_TOKEN = auth.OAuthSession().auth()



def get_backup_ids(file="raw_queue.txt", completed_file="completed"):
    """Return list of ungraded submission ids.

    Keyword arguments:
    file -- the file path to the list of submission URLs (default "raw_queue.txt")
    completed_file -- the file path to the list of completed submission IDs (default "completed")
    """

    with open(file, "r+") as f, open(completed_file) as g:
        text = f.read()
        ids = re.findall(r"/composition/(.+)\?", text)
        completed_ids = [id.strip() for id in g]
        ids = [id for id in ids if id not in completed_ids]
        f.seek(0)
        f.write(
            "\n".join(
                f"https://okpy.org/admin/composition/{id}?diff=full" for id in ids
            )
        )
        f.truncate()
        return ids


def get_backup_code(id):
    """Returns the code to be reviewed.

    Arguments:
    id -- the id of the submission to be graded.
    """

    params = {"access_token": ACCESS_TOKEN}
    r = requests.get(f"https://okpy.org/api/v3/backups/{id}", params=params)
    messages = r.json()["data"]["messages"]
    out = None
    for message in messages:
        #TODO: Change references to ants.py when the project changes
        if "ants.py" in message["contents"]:
            if out is not None:
                raise Exception("Multiple ants.py found???")
            out = message["contents"]["ants.py"]

    if out is None:
        raise Exception("No ants.py found!!!")

    return out


def submit_comment(id, line, message):
    """Submits comment to okpy.

    Arguments:
    id -- Submission ID to comment on
    line -- Line number to comment on
    message -- Comment message
    """

    params = {"access_token": ACCESS_TOKEN}
    #TODO: Change reference to ants.py when the project changes
    data = {"filename": "ants.py", "line": line, "message": message}
    r = requests.post(
        f"https://okpy.org/api/v3/backups/{id}/comment/", params=params, data=data
    )
    assert r.status_code == 200, "fail"


def submit_grade(id, score, message, completed="completed"):
    """Submits composition grade to okpy.

    Arguments:
    id -- Submission ID to grade
    score -- Composition score recieved
    message -- Final message to send
    completed -- File with list of graded IDs.
    """

    params = {"access_token": ACCESS_TOKEN}
    data = {"bid": id, "kind": "composition", "score": score, "message": message}
    r = requests.post(f"https://okpy.org/api/v3/score/", params=params, data=data)
    assert r.status_code == 200, "fail"
    webbrowser.open(f"https://okpy.org/admin/composition/{id}")
    with open(completed, "a") as f:
        f.write(id + "\n")
