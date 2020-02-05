# Composition Assistant

## Getting Started
1. Clone the repository: `git clone https://github.com/Cal-CS-61A-Staff/composition-assistant.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Update raw_queue.txt with the submissions you are assigned.
3. Run the command line interface: `python3 cli.py`

## Video Tutorial
A video (silent) tutorial can be found here: https://drive.google.com/file/d/1yJVNBHJ-S0ZRXTVJ8Smw6NZtpPW0VOm6/view

## Using the command line interface
1. Sign in with Okpy account
2. Follow on screen instructions

Types of comments available to you can be found in template.py

## File Description
- Pipfile: Python dependencies file
- README.md: This document!
- analyzer.py: Main part of the analyzer program
- auth.py: OK authentication.
- cli.py: Command Line Interface. Run this program.
- completed: List of submission IDs that have been graded.
- finalizing.py: Final comments and composition score.
- ok: OK binary file
- ok_interface.py: Interfaces with OK (Pulls submissions and sends comments and grades).
- raw_queue.txt: List of submissions to grade for composition. Copy the HTML source of the OKPy `grading queue` into this file and the submissions will be automatically extracted.
- requirements.txt: Python dependencies file. Used to run pip install.
- secrets.py: OK access token
- templates.py: List of possible comments.
