from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import Expense, Category
from sqlalchemy.sql import func
from datetime import datetime

@app.route("/")
def home():
    return render_template("home.html") 

@app.route("/expenses")
def expenses():
    expenses = Expense.query.all()
    return render_template("index.html", expenses=expenses)


@app.route("/overview")
def overview():
    # Add logic to fetch and pass data to the template if needed
    return render_template("overview.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Add logic to handle login (authentication)
        pass
    return render_template("login.html")

@app.route('/logout')
def logout():
    # Your logout logic here
    # For example, if using Flask-Login:
    # logout_user()
    return redirect(url_for('home'))



## CATEGORIES ##

@app.route("/categories")
def categories():
    categories = Category.query.order_by(Category.priority).all()
    return render_template("categories.html", categories=categories)


@app.route("/get_categories", methods=["GET"])
def get_categories():
    categories = Category.query.order_by(Category.priority).all()
    return jsonify(categories=[category.serialize for category in categories])  

@app.route("/edit_category", methods=["POST"])
def edit_category():
    data = request.get_json()
    category_id = data.get('id')
    field = data.get('field')
    new_value = data.get(field)
    
    category = Category.query.get_or_404(category_id)
    if field == 'name':
        category.name = new_value
    elif field == 'budget':
        category.budget = new_value
    db.session.commit()
    
    return jsonify({'success': True})



@app.route("/add_category", methods=["POST"])
def add_category():
    name = request.form.get("name")
    budget = request.form.get("budget")
    # Assign the next priority
    max_priority = db.session.query(db.func.max(Category.priority)).scalar() or 0
    if name and budget:
        currency = request.form.get("currency")
        category = Category(name=name, budget=budget, currency=currency, priority=max_priority+1)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully!", "success")
        return redirect(url_for("categories"))
    else:
        return "Error", 400

@app.route("/reorder_categories", methods=["POST"])
def reorder_categories():
    order = request.form.getlist("order[]")
    if order:
        for index, id in enumerate(order, 1):
            category = Category.query.get(id)
            category.priority = index
        db.session.commit()
        flash("Categories reordered successfully!", "success")
        return redirect(url_for("categories"))
    else:
        return "Error", 400
    
@app.route("/delete_category", methods=["POST"])
def delete_category():
    data = request.get_json()
    category_id = data.get('id')
    
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'success': True})






@app.route("/delete_expense/<int:id>", methods=["POST"])
def delete_expense(id):
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully!", "success")
    return redirect(url_for("expenses"))


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
    name = request.form["name"]
    currency = request.form["currency"]
  # Check if "recurring" key exists in the form data
    recurring = request.form.get("recurring", None)

# If it doesn't exist, recurring will be None or you can set a default value

    date_str = request.form.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.utcnow()

    expense = Expense(name=name, currency=currency, recurring=recurring, category=category, amount=amount, date=date)
    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!", "success")
    return redirect(url_for("expenses"))
