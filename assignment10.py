

import re
from flask import Flask, render_template, request

app = Flask(__name__)

GUESTBOOK_FILE = "guestbook.txt"


BAD_WORDS_PATTERN = re.compile(r"\b(darn|heck|shoot)\b", re.IGNORECASE)


def censor_message(message):
    """Replaces any bad word (case-insensitive, whole word) with ***."""
    return BAD_WORDS_PATTERN.sub("***", message)


def load_messages():
    """
    Reads guestbook.txt and returns a list of its lines (messages).
    Returns an empty list if the file doesn't exist yet.
    """
    try:
        with open(GUESTBOOK_FILE, "r", encoding="utf-8") as f:
            # strip() removes the trailing newline from each line
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        message = request.form.get("message", "").strip()

        # Only save if both fields actually have content
        if username and message:
            cleaned_message = censor_message(message)

            # Append the new entry to the guestbook file
            with open(GUESTBOOK_FILE, "a", encoding="utf-8") as f:
                f.write(f"{username}: {cleaned_message}\n")

    # Whether GET or POST, load the current list of messages to display
    messages = load_messages()
    return render_template("index.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)