import argparse

parser = argparse.ArgumentParser(description='Enter project endpoint')
parser.add_argument("proj", help="Run 'python3 cli.py <proj>', where <proj> is one of the following: hog cats ants scheme")
args = parser.parse_args()

with open('proj.txt', 'w') as f:
    f.write(args.proj)

import os
import re
import sys
import traceback
import readline
from typing import NamedTuple, List

from PyInquirer import prompt
from pygments import highlight
from pygments.formatters.terminal import TerminalFormatter
from pygments.lexers.python import PythonLexer

from analyzer import get_problems, Comment
from finalizing import grade
from ok_interface import get_backup_ids, get_backup_code, submit_comment, submit_grade
from colorama import Fore, Style

from templates import template_completer, templates


class Grade(NamedTuple):
    score: int
    message: str
    comments: List[Comment]


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def display_code_with_accepted_and_potential_comments(
    name, problem, accepted_comments, curr_comment=None
):
    clear()
    print(f"Problem: {name}")
    highlighted_code = highlight(problem.code, PythonLexer(), TerminalFormatter())
    for i, line in enumerate(highlighted_code.split("\n")):
        line_num = problem.initial_line_number + i
        if line_num in accepted_comments or (
            curr_comment and line_num == curr_comment.line_num
        ):
            print()
        print(f"{Fore.GREEN}{line_num} {Style.RESET_ALL}{line}")
        if line_num in accepted_comments or (
            curr_comment and line_num == curr_comment.line_num
        ):
            indent_level = len(line) - len(line.strip()) + 3
            if line_num in accepted_comments:
                for accepted_comment in accepted_comments[line_num]:
                    print(
                        Fore.MAGENTA
                        + " " * indent_level
                        + "# "
                        + accepted_comment.comment
                    )
            if curr_comment and line_num == curr_comment.line_num:
                print(
                    Fore.RED
                    + Style.BRIGHT
                    + " " * indent_level
                    + "# "
                    + curr_comment.comment
                )
            print()
    print()


def complete(comment):
    if comment.fields:
        print("Please provide supplementary information:")
    field_vals = {}
    for field in comment.fields:
        q = {"type": "input", "name": "field", "message": field + ":"}
        response = wrapped_prompt(q)
        field_vals[field] = response["field"]

    complete_text = comment.comment.format(**field_vals)
    q = {
        "type": "input",
        "name": "final",
        "message": "Final message",
        "default": complete_text,
    }
    response = wrapped_prompt(q)

    return Comment(comment.line_num, response["final"])


def add_comment(accepted_comments, new_comment):
    if not new_comment:
        return
    if new_comment.line_num not in accepted_comments:
        accepted_comments[new_comment.line_num] = []
    accepted_comments[new_comment.line_num].append(new_comment)


class Interrupt(Exception):
    def __init__(self, cmd):
        super()
        self.cmd = cmd


def wrapped_prompt(q):
    ret = prompt([q])
    if not ret:
        receive_command()
    return ret


def wrapped_input(q):
    try:
        ret = input(q)
    except KeyboardInterrupt:
        return receive_command()
    return ret


def receive_command():
    inp = input(
        f"\n\n"
        f"cancel = cancel this comment\n"
        f"clear = clear all question comments\n"
        f"reset = reset all student comments\n"
        f"? {Style.BRIGHT}{Fore.RED}command: {Style.RESET_ALL}"
    )
    raise Interrupt(inp)


def main():
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims("")
    print("cli.py main")
    for id in get_backup_ids():
        try:
            code = get_backup_code(id)
            problems = get_problems(code)
        except Exception:
            print(
                f"{Fore.RED}An exception occurred while processing backup id #{id}",
                file=sys.stderr,
            )
            traceback.print_exc(file=sys.stderr)
            print(f"{Style.RESET_ALL}")
            continue

        grade = grade_backup(problems)
        for comment in grade.comments:
            print(comment)
            assert not comment.fields, "fields not substituted!"
            submit_comment(id, comment.line_num, comment.comment)
        submit_grade(id, grade.score, grade.message)


def grade_backup(problems):
    comments = []
    try:
        for name, problem in problems.items():
            comments.extend(grade_problem(name, problem))
        score, message = grade(comments)
        print(message)
        q = {
            "type": "confirm",
            "name": "ok",
            "message": "Does this grade look reasonable?",
        }
        response = wrapped_prompt(q)
        return Grade(score, message, comments)
    except Interrupt as e:
        if e.cmd == "reset":
            return grade_backup(problems)
        raise


def grade_problem(name, problem):
    readline.set_completer(template_completer(name))

    try:
        accepted_comments = {}
        for comment in problem.comments:
            try:
                display_code_with_accepted_and_potential_comments(
                    name, problem, accepted_comments, comment
                )
                print(f"{Fore.CYAN}Potential comment: {Style.RESET_ALL}")
                print(
                    f"{Fore.GREEN}{comment.line_num}{Style.RESET_ALL} {comment.comment}"
                )
                q = {
                    "type": "confirm",
                    "name": "ok",
                    "message": "Add comment",
                    "default": True,
                }
                response = wrapped_prompt(q)
                if response["ok"]:
                    add_comment(accepted_comments, complete(comment))
            except Interrupt as e:
                if e.cmd == "cancel":
                    continue
                raise

        while True:
            try:
                display_code_with_accepted_and_potential_comments(
                    name, problem, accepted_comments
                )
                response = wrapped_input(
                    f"? {Style.BRIGHT} Custom comment type: {Style.RESET_ALL}"
                )
                if not response:
                    q = {
                        "type": "confirm",
                        "name": "ok",
                        "message": "Go to next question?",
                        "default": True,
                    }
                    response = wrapped_prompt(q)
                    if response["ok"]:
                        break
                    continue
                if response not in templates:
                    print(
                        f"{Fore.RED} Template {response} not found! {Style.RESET_ALL}"
                    )
                    continue
                text = templates[response]
                q = {"type": "input", "name": "line_num", "message": "Line number:"}
                response = wrapped_prompt(q)
                try:
                    line_num = int(response["line_num"])
                except ValueError:
                    print(
                        f"{Fore.RED} Expected a number, received {response['line_num']} not found! {Style.RESET_ALL}"
                    )
                    continue

                if text:
                    fields = list(set(re.findall(r"{(.*?)}", text)))
                    comment = Comment(line_num, text, fields)
                    add_comment(accepted_comments, complete(comment))
                else:
                    q = {"type": "input", "name": "text", "message": "Comment:"}
                    response = wrapped_prompt(q)
                    comment = Comment(line_num, response["text"], [])
                    add_comment(accepted_comments, comment)
            except Interrupt as e:
                if e.cmd == "cancel":
                    continue
                raise
        print()

        return list(sum(accepted_comments.values(), []))

    except Interrupt as e:
        if e.cmd == "clear":
            return grade_problem(name, problem)
        raise


if __name__ == "__main__":
    try:
        main()
    except:
        print(f"{Style.RESET_ALL}")
