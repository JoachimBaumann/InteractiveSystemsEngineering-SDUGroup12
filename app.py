from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
from sqlalchemy.sql import func

app = Flask(__name__)
app.secret_key = "some_random_string_here"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


@app.route("/")
def hello():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Expense('{self.category}', '{self.amount}', '{self.date}')"


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

    return jsonify({"categories": categories, "amounts": amounts})


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


if __name__ == "__main__":
    app.run(debug=True)
