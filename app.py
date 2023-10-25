from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from sqlalchemy.sql import func


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


@app.route("/")
def hello():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    # Fetch date from the form or use current date
    date = request.form.get("date", datetime.utcnow())

    expense = Expense(category=category, amount=amount, date=date)
    db.session.add(expense)
    db.session.commit()
    return redirect(url_for("hello"))


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Expense('{self.category}', '{self.amount}', '{self.date}')"


if __name__ == "__main__":
    app.run(debug=True)


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    date = request.form.get("date", datetime.utcnow())

    expense = Expense(category=category, amount=amount, date=date)
    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!", "success")
    return redirect(url_for("hello"))


@app.route("/delete_expense/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("hello"))


@app.route("/expense_data", methods=["GET"])
def expense_data():
    data = (
        db.session.query(Expense.category, func.sum(Expense.amount))
        .group_by(Expense.category)
        .all()
    )
    categories = [item[0] for item in data]
    amounts = [item[1] for item in data]
    return {"categories": categories, "amounts": amounts}


@app.route("/expense_data")
def expense_data():
    categories = [expense.category for expense in Expense.query.all()]
    amounts = [expense.amount for expense in Expense.query.all()]

    data = {
        "categories": list(set(categories)),
        "amounts": [
            sum(
                amount
                for category, amount in zip(categories, amounts)
                if category == cat
            )
            for cat in set(categories)
        ],
    }

    return jsonify(data)


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category = request.form["category"]
    amount = request.form["amount"]
    date_str = request.form.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.utcnow()

    expense = Expense(category=category, amount=amount, date=date)
    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!", "success")
    return redirect(url_for("hello"))
