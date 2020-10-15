MESSAGES = [
    "0 - Good job. I've suggested a few improvements in the comments to fix. You can get full credit for composition "
    "if you go back and revise the code to address the comments and then run `python3 ok --revise`. You can learn more "
    "about 61A composition guidelines at https://cs61a.org/articles/composition.html",
    "1 - Good job, the code is nicely organized and easy to read. There were a few minor issues that should be fixed. "
    "You can get full credit for composition if you go back and revise the code to address the comments and then run "
    "`python3 ok --revise`. You can learn more about 61A composition guidelines "
    "at https://cs61a.org/articles/composition.html",
    "2 - Great work! I've suggested a few changes that you should look at for future improvement. "
    "You can learn more about 61A composition guidelines at https://cs61a.org/articles/composition.html",
]


def grade(comments):
    if len(comments) < 2:
        score = 2
    elif len(comments) < 10:
        score = 1
    else:
        score = 0

    return score, MESSAGES[score] 
