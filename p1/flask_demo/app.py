# CTI 110
# P1LAB2 demo - Selling Things, as a web app
# norrisa

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def store():
    if request.method == "GET":
        return render_template("store.html")

    # INPUT (from the form instead of input())
    product_name = request.form.get("product_name", "")
    count_text = request.form.get("product_count", "")
    price_text = request.form.get("product_price", "")

    # PROCESSING
    try:
        product_count = int(count_text)
        product_price = float(price_text)
    except ValueError:
        return render_template(
            "store.html",
            error="Count must be a whole number and price must be a decimal number.",
            product_name=product_name,
            product_count=count_text,
            product_price=price_text,
        )

    total = product_count * product_price

    # OUTPUT
    return render_template(
        "store.html",
        product_name=product_name,
        product_count=product_count,
        product_price=product_price,
        total=total,
        show_receipt=True,
    )


if __name__ == "__main__":
    app.run(debug=True)
