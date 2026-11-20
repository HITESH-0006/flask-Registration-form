import re

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")


def validate(form):
    """Return (cleaned_data, errors) for the submitted registration form."""
    data = {
        "name": form.get("name", "").strip(),
        "city": form.get("city", "").strip(),
        "phone": form.get("phone", "").strip(),
    }
    errors = {}

    if not data["name"]:
        errors["name"] = "Enter your name."
    elif len(data["name"]) > 100:
        errors["name"] = "Name must be 100 characters or fewer."

    if not data["city"]:
        errors["city"] = "Enter your city."
    elif len(data["city"]) > 100:
        errors["city"] = "City must be 100 characters or fewer."

    digits_only = re.sub(r"[\s\-()]", "", data["phone"])
    if not data["phone"]:
        errors["phone"] = "Enter your phone number."
    elif not PHONE_PATTERN.match(digits_only):
        errors["phone"] = "Enter a valid phone number (10 to 15 digits)."

    return data, errors


@app.route("/")
def index():
    return render_template("register.html", data={}, errors={})


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "GET":
        return redirect(url_for("index"))

    data, errors = validate(request.form)
    if errors:
        return render_template("register.html", data=data, errors=errors), 400
    return render_template("confirmation.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
