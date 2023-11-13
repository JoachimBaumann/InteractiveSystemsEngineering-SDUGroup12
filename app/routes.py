from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import Expense, Category
from sqlalchemy.sql import func
from datetime import datetime, date
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import logging


@app.route('/')
def index():
    return render_template('login.html')


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
    return redirect(url_for('index'))


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
    # Redirect to the page where expenses are listed after deletion.
    return redirect(url_for("expenses"))

@app.route("/expense_data", methods=["GET"])
def expense_data():
    data = (
        db.session.query(Expense.category_id, func.sum(Expense.amount))
        .join(Category, Expense.category_id == Category.id)
        .group_by(Expense.category_id)
        .all()
    )
    categories = [Category.query.get(item[0]).name for item in data]  # Assure this line gets the category name properly
    amounts = [item[1] for item in data]

    return jsonify({"categories": categories, "amounts": amounts})


@app.route("/add_expense", methods=["POST"])
def add_expense():
    category_id = request.form["category"]
    amount = request.form["amount"]
    name = request.form["name"]
    currency = request.form["currency"]
    recurring = request.form.get("recurring", "No")  # Set default to "No" if not provided

    # Find the category object based on the ID provided
    category = Category.query.get(category_id)
    if not category:
        flash(f"Category with ID '{category_id}' not found!", "danger")
        return redirect(url_for("expenses"))  # Redirect to the expenses page if category not found

    date_str = request.form.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.utcnow()

    # Create a new Expense object using the category_id
    expense = Expense(name=name, currency=currency, recurring=recurring, category_id=category.id, amount=amount, date=date)
    db.session.add(expense)
    db.session.commit()

    flash("Expense added successfully!", "success")
    # Redirect to the page where expenses are listed after adding.
    return redirect(url_for("expenses"))



@app.route('/expenses')
def expenses():
    categories = Category.query.all()  # Assuming you have a Category model.
    expenses = Expense.query.all()  # If you want to list all expenses on the same page.
    return render_template("expenses.html", categories=categories, expenses=expenses)

# This is an example in Python using Flask*----------------------------------------------------------------------------------------

def get_spending_data(start_date, end_date, category_id=None):
    query = db.session.query(
        Expense.date, func.sum(Expense.amount).label('amount')
    ).filter(
        Expense.date >= start_date, Expense.date <= end_date
    )
    if category_id is not None:
        query = query.filter(Expense.category_id == category_id)

    return query.group_by(Expense.date).all()

def calculate_forecast_spending(start_date, end_date, category_id=None):
    # Start of the current month
    current_month_start = date.today().replace(day=1)

    # Get spending data for the current month up to yesterday
    past_spending_data = get_spending_data(current_month_start, date.today() - timedelta(days=1), category_id)

    # Calculate total spending and average daily spending
    total_spending = sum([record.amount for record in past_spending_data])
    num_days_past = (date.today() - current_month_start).days
    average_daily_spending = total_spending / num_days_past if num_days_past > 0 else 0

    # Create forecast data for the entire current month
    total_days_in_month = (date(current_month_start.year, current_month_start.month + 1, 1) - timedelta(days=1)).day
    forecast_spending = 0
    forecast_values = []

    for day in range(1, total_days_in_month + 1):
        forecast_spending += average_daily_spending
        forecast_values.append(forecast_spending)

    # Generate labels for the entire current month
    labels = [(current_month_start + timedelta(days=i - 1)).strftime('%Y-%m-%d') for i in range(1, total_days_in_month + 1)]

    return {'labels': labels, 'values': forecast_values}

@app.route('/get-forecast-spending', methods=['POST'])
def get_forecast_spending():
    try:
        data = request.get_json()
        category_id = data.get('categoryId')

        # Set start and end dates to cover the entire current month
        start_date = date.today().replace(day=1)
        end_date = date(start_date.year, start_date.month + 1, 1) - timedelta(days=1)

        forecast_data = calculate_forecast_spending(start_date, end_date, category_id)

        return jsonify(forecast_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/get-category-data/<int:category_id>')
def get_category_data(category_id):
    try:
        category = Category.query.get(category_id)
        if not category:
            return jsonify({'error': f'Category with ID {category_id} not found'}), 404
        total_expenses = db.session.query(func.sum(Expense.amount)).filter(Expense.category_id == category_id).scalar() or 0
        remainder = category.budget - total_expenses
        data = {'budget': category.budget, 'expenses': total_expenses, 'remainder': remainder}
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-all-categories-data')
def get_all_categories_data():
    try:
        total_budget = db.session.query(func.sum(Category.budget)).scalar() or 0
        total_expenses = db.session.query(func.sum(Expense.amount)).scalar() or 0
        total_remainder = total_budget - total_expenses
        data = {'totalBudget': total_budget, 'totalExpenses': total_expenses, 'totalRemainder': total_remainder}
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-in-progress-spending', methods=['POST'])
def get_in_progress_spending():
    try:
        data = request.get_json()
        start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
        end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
        category_id = data.get('categoryId')
        spending_data = get_spending_data(start_date, end_date, category_id)
        labels = [record.date.strftime('%Y-%m-%d') for record in spending_data]
        values = [float(record.amount) for record in spending_data]
        return jsonify({'labels': labels, 'values': values})
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/overview')
def overview():
    try:
        categories = Category.query.order_by(Category.name).all()
        all_categories_data = get_all_categories_data().get_json()

        start_date = datetime.now().replace(day=1)
        end_date = start_date + relativedelta(months=1, days=-1)

        in_progress_data = get_spending_data(start_date, end_date)
        # Ensure calculate_forecast_spending is implemented or handle it appropriately
        forecast_data = calculate_forecast_spending(start_date, end_date)
        context = {
        'categories': categories,
        'totalBudget': all_categories_data['totalBudget'],
        'totalExpenses': all_categories_data['totalExpenses'],
        'totalRemainder': all_categories_data['totalRemainder'],
        'inProgressLabels': [record.date.strftime('%Y-%m-%d') for record in in_progress_data],
        'inProgressValues': [float(record.amount) for record in in_progress_data],
        # Assuming calculate_forecast_spending returns a dictionary with labels and values
        'forecastLabels': forecast_data['labels'] if forecast_data else [],
        'forecastValues': forecast_data['values'] if forecast_data else []
        }

        return render_template("overview.html", **context)
    except Exception as e:
        return jsonify({'error': str(e)}), 500