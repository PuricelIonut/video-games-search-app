import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, get_game_description, search_game, get_game_screenshots

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Store db
db = SQL("sqlite:///users.db")

# Make sure API key is set and store it inside variable
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["POST", "GET"])
@login_required
def index():

    user_id = session["user_id"]
    game_collection = db.execute("SELECT game_name FROM my_collection WHERE user_id = ?", user_id)
    game_list = []

    for key in game_collection:
        game_list.append(key["game_name"])

    if request.method == "POST":

        # Store form input
        search_string = request.form.get("search")

        # Search game to get slug
        game_search = search_game(search_string)

        # Check for valid input
        try:
            slug = game_search["results"][0]["slug"]
        except IndexError:
            flash("Invalid game name.Try again!")
            return render_template("index.html")

        # Game name validation
        if slug is None:
            flash("Invalid game name.Try again!")
            return render_template("index.html")

        # Get game description and screenshots by that exact slug
        screenshots = get_game_screenshots(slug)
        data_json = get_game_description(slug)

        return render_template("search.html", game_collection=game_list, game=data_json, screen_s=screenshots["results"])
    else:
        return render_template("index.html")


@app.route("/search")
@login_required
def search():
    return redirect("/")


@app.route("/collection", methods=["POST", "GET"])
@login_required
def collection():

    # Get user id and game names from db
    user_id = session["user_id"]
    game_collection = db.execute("SELECT * FROM my_collection WHERE user_id = ?", user_id)

    if request.method == "POST":

        # Update progress
        if request.form.get("progress") is not None:
            db.execute("UPDATE my_collection SET progress = ? WHERE user_id = ? AND game_name = ?",
                       request.form.get("progress"), user_id, request.form.get("progress_list"))
        # Delete game
        if request.form.get("delete") is not None:
            db.execute("DELETE FROM my_collection WHERE user_id = ? AND game_name = ?",
                       user_id, request.form.get("delete"))

        # Add game to db
        if request.form.get("game_name") is not None:
            db.execute("INSERT INTO my_collection (game_name, user_id) VALUES(?,?)",
                       request.form.get("game_name"), user_id)

        return redirect("/collection")
    else:
        return render_template("collection.html", game_collection=game_collection)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_idjec
    session.clear()

    # Check db for username
    data = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username exists and password is correct
        if len(data) != 1 or not check_password_hash(data[0]["hash"], request.form.get("password")):
            flash("Username/password not registered!")
            return render_template("login.html")

        # Remember which user logged in
        session["user_id"] = data[0]["id"]
        session["username"] = data[0]["username"]
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():

    # Get username from db
    data = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    if request.method == "POST":

        # Validate form
        if request.form.get("password") != request.form.get("confirmation"):
            flash("Passwords do not match!")
            return render_template("register.html")
        elif len(data) == 1:
            flash("Username taken!")
            return render_template("register.html")

        # Hash password and store in db
        hash_password = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash_password)

        return redirect("/")
    else:
        return render_template("register.html")


@app.route("/change", methods=["GET", "POST"])
def change():

    # Get username from db
    data = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

    if request.method == "POST":

        # Check if username and pw in db
        if len(data) != 1 or not check_password_hash(data[0]["hash"], request.form.get("password")):
            flash("Invalid username/password")
            return render_template("change.html")

        # Check if new pw match
        elif request.form.get("new_pw") != request.form.get("new_pw_conf"):
            flash("Passwords not matching")
            return render_template("change.html")

        # Hash new pw and change old pw
        new_pw = generate_password_hash(request.form.get("new_pw"))
        db.execute("UPDATE users SET hash = ? WHERE username = ?", new_pw, request.form.get("username"))

        return logout()
    else:
        return render_template("change.html")


if __name__ == "__main__":
    app.run(debug=True)