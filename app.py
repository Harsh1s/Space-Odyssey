import logging
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, redirect, render_template, request, session
from flask_session import Session

from csv_functions import check_user_exists_in_csv, header, write_to_csv
from firebase_functions import (
    check_password,
    get_ordered_list_of_users_based_on_points,
    get_team_details,
    get_team_dict,
    initialize_firebase_for_a_user,
    update_team_details,
)
from miscellaneous import *
from questions import (
    answerify,
    generate_sequence_for_a_team,
    get_personal_current_question,
    hint_used,
    perhaps_completed,
)
from spreadsheet import write_to_gsheet

# Initialize Flask app
app = Flask("Space Odessey " + __name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


def has_event_ended() -> bool:
    return False


@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
@app.route("/index", methods=["GET"])
def index_page():
    return render_template("index.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    message = ""
    if request.method == "POST":
        data = dict()
        data["name"] = request.form["name"]
        data["regno"] = request.form["regno"].casefold()
        data["email"] = request.form["email"]
        data["password"] = hasher(request.form["password"])
        data["phone"] = int(request.form["phone"])
        data["receiptno"] = int(0)

        data["uniqid"] = generate_uuid()
        team_sequence = generate_sequence_for_a_team()
        data["current_question"] = 1
        data["sequence"] = str(team_sequence)
        data["hint_used"] = False
        data["hints_used"] = "[0]"
        print(data["regno"] + " - " + data["name"], "tried to register")
        if check_user_exists_in_csv(data["regno"], data["uniqid"]):
            message = "You have already registered!"
            if not get_team_dict(data["regno"]):
                message = "Error in registering"
        else:
            row = [
                data["name"],
                data["regno"],
                data["email"],
                data["password"],
                data["phone"],
                data["receiptno"],
                data["uniqid"],
                str(data["sequence"]),
                data["current_question"],
            ]
            write_to_gsheet(
                row=row, spreadsheet_id=os.getenv("REGISTRATIONS_SPREADSHEET")
            )
            initialize_firebase_for_a_user(data)
            write_to_csv(data, filename="spaceRegistrations.csv", row=row)
            print(f"Added {row}")
            session["name"] = data["name"]
            session["regno"] = data["regno"]
            session["uniqid"] = data["uniqid"]
            session["current_question"] = data["current_question"]
            message = "You have successfully registered"
        return render_template(
            "register.html",
            yet_to_register=False,
            show_message=message,
        )
    # 👇 Requested /register in a get method, return normally
    return render_template("register.html", yet_to_register=True, show_message=message)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        regno = request.form["regno"].upper()
        if "@" in regno:
            return render_template("login.html", show_message="Invalid Credentials")
        hashed_pw = hasher(request.form["password"])
        print(regno + " - " + hashed_pw, "tried to login")
        if check_password(regno, hashed_pw):
            session.clear()
            d = get_team_dict(regno)
            session["name"] = d["name"]
            session["regno"] = d["regno"]
            session["uniqid"] = d["uniqid"]
            session["current_question"] = d["current_question"]
            print(
                f"User {session['regno']} has logged in, is on {session['current_question']} question"
            )
            return redirect("/play")

        else:
            return render_template("login.html", show_message="Invalid Credentials")
    return render_template("login.html", show_message="")


@app.route("/play", methods=["POST", "GET"])
def play():
    # if not logged in, redirect to login page
    if "regno" not in session:
        print("Not logged in and tried to access play")
        return redirect("/logout")

    show_name = session["name"] if "name" in session else session["regno"]

    attempted_correct = [False, False]

    if perhaps_completed(session["regno"], session["current_question"]):
        return redirect("/completed")

    ques = get_personal_current_question(regno=session["regno"])

    # Post method, meaning sent answer, didn't request page. Just calculates whether right answer or not and returns the page.
    if request.method == "POST":
        attempted_correct[0] = True
        submitted_answer = request.form["answer"]
        submitted_key = "KEY1234"

        if answerify(submitted_answer) == ques.answer and answerify(
            submitted_key
        ) == answerify(ques.key):
            attempted_correct[1] = True
            cq = int(get_team_details(session["regno"], "current_question"))
            cq += 1
            session["current_question"] = str(cq)
            update_team_details(session["regno"], "current_question", cq)
            ques = get_personal_current_question(regno=session["regno"])
            update_team_details(session["regno"], "hint_used", "False")
            submitted_key = ""
        else:
            attempted_correct[1] = False
        if perhaps_completed(session["regno"], session["current_question"]):
            return redirect("/completed")

        return render_template(
            "play.html",
            show_name=show_name,
            attempted_correct=attempted_correct,
            q_type=ques.type,
            question=ques.text,
            location=ques.location,
            last_key=submitted_key,
        )

    # if already logged in, redirect to play page
    # Display the current question
    update_team_details(session["regno"], "hint_used", "False")
    return render_template(
        "play.html",
        show_name=show_name,
        attempted_correct=attempted_correct,
        q_type=ques.type,
        question=ques.text,
        location=ques.location,
        last_key="",
    )


@app.route("/hints", methods=["POST"])
def hints():
    # if not logged in, redirect to login page
    if "regno" not in session:
        print("Not logged in and tried to access play")
        return redirect("/logout")
    ques = get_personal_current_question(regno=session["regno"])
    hint = ques.hint
    hint_used(session["regno"])
    if hint:
        return jsonify({"hint": str(hint)})
    return jsonify({"hint": "Hint not found/Does not exist for this question"})


@app.route("/completed", methods=["GET"])
def completed():
    if "current_question" in session:
        if perhaps_completed(session["regno"], session["current_question"]):
            return render_template("completed.html")
    return redirect("/play")


@app.route("/leaderboard")
def leaderboard():
    ordered_list = get_ordered_list_of_users_based_on_points()
    return render_template("leaderboard.html", ordered_list=ordered_list)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


load_dotenv("space-odyssey.env")

if __name__ == "__main__":
    port = int(os.getenv("PORT")) if os.getenv("PORT") else 8080
    app.run(debug=bool(os.getenv("DEBUG")), host="0.0.0.0", port=port)
