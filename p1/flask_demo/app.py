# CTI 110
# P1LAB2 demo - Selling Things, as a web app
# norrisa

# WHAT THIS TEACHES
#   - The same INPUT / PROCESSING / OUTPUT program as P1LAB2, but the user
#     types into a web form instead of a terminal.
#   - A web app is a function that answers a request. The browser asks;
#     the function replies with a page.
#   - GET means "show me the page". POST means "here is my form data".
#   - Bad input should produce a polite message, not a crash.
#
# To run it (needs Flask installed):   cd p1/flask_demo && python3 app.py
# Then open http://127.0.0.1:5000 in a browser.
# The page itself lives in templates/store.html. Flask looks for HTML in a
# folder named "templates". The folder name is not a suggestion.

from flask import Flask, render_template, request

# Make the app object. __name__ tells Flask where to find the templates folder.
app = Flask(__name__)


# @app.route is a decorator. It says: "when the browser asks for the
# address /, run the function just below." One function, two kinds of visit.
@app.route("/", methods=["GET", "POST"])
def store():
    # First visit (typing the address) is a GET. Show the empty form and stop.
    if request.method == "GET":
        return render_template("store.html")

    # Pressing the button sends a POST. Read the three form fields.
    # INPUT (from the form instead of input())
    # .get(name, "") returns "" instead of crashing if the field is missing.
    product_name = request.form.get("product_name", "")
    count_text = request.form.get("product_count", "")
    price_text = request.form.get("product_price", "")

    # Form values arrive as text, just like input() gave us text.
    # PROCESSING
    # try/except: attempt the conversions. If either one fails, jump to except.
    try:
        product_count = int(count_text)
        product_price = float(price_text)
    except ValueError:
        # Show the form again with an error and the user's own typing,
        # so they fix one mistake instead of retyping everything.
        return render_template(
            "store.html",
            error="Count must be a whole number and price must be a decimal number.",
            product_name=product_name,
            product_count=count_text,
            product_price=price_text,
        )

    total = product_count * product_price

    # OUTPUT
    # Each keyword argument becomes a variable the template can use, like
    # {{ total }}. show_receipt switches on the receipt section of the page.
    return render_template(
        "store.html",
        product_name=product_name,
        product_count=product_count,
        product_price=product_price,
        total=total,
        show_receipt=True,
    )


# This is true only when you run THIS file directly, not when it is imported.
# debug=True reloads the server when you save, and shows errors in the
# browser. Fine in class. Never leave it on for a real website.
if __name__ == "__main__":
    app.run(debug=True)
