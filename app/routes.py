from flask import render_template, request, redirect, url_for, flash, jsonify
from app import app, db
from app.models import Expense, Category
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


@app.route('/')
def index():
    return render_template('login.html')



@app.route("/overview")
def overview():
    # Query all categories from the database
    categories = Category.query.order_by(Category.name).all()
    
    # Fetch the default "All Categories" data
    all_categories_data = get_all_categories_data().get_json()
    
    # Set up default date range (e.g., current month)
    start_date = datetime.now().replace(day=1)
    end_date = (start_date + relativedelta(months=1)) - timedelta(days=1)
    
    # Get initial in-progress spending data
    in_progress_data = calculate_in_progress_spending(start_date, end_date, None)

    # Get initial forecast spending data
    forecast_data = calculate_forecast_spending(start_date, end_date, None)

    # Prepare your context data for the template, including the initial chart data
    context = {
        'categories': categories,
        'totalBudget': all_categories_data['totalBudget'],
        'totalExpenses': all_categories_data['totalExpenses'],
        'totalRemainder': all_categories_data['totalRemainder'],
        'inProgressLabels': in_progress_data['labels'],
        'inProgressValues': in_progress_data['values'],
        'forecastLabels': forecast_data['labels'],
        'forecastValues': forecast_data['values'],
    }
    # Pass the context to the template
    return render_template("overview.html", **context, in_progress_data=in_progress_data, forecast_data=forecast_data)

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

# This is an example in Python using Flask

@app.route('/get-category-data/<int:category_id>')
def get_category_data(category_id):
    # Fetch the category using the category_id
    category = Category.query.get_or_404(category_id)

    # Calculate the total expenses for this category
    total_expenses = db.session.query(func.sum(Expense.amount)).filter(Expense.category_id == category_id).scalar()
    total_expenses = total_expenses or 0  # if there are no expenses, default to 0

    # Calculate the remainder of the budget
    remainder = category.budget - total_expenses

    # Prepare the data dictionary with actual values
    data = {
        'budget': category.budget,
        'expenses': total_expenses,
        'remainder': remainder
    }

    return jsonify(data)


@app.route('/get-all-categories-data')
def get_all_categories_data():
    # Query that sums all budgets for all categories
    total_budget = db.session.query(db.func.sum(Category.budget)).scalar() or 0
    # Query that sums all expenses for all categories by joining Expense and Category tables
    total_expenses = db.session.query(db.func.sum(Expense.amount)).scalar() or 0
    # Calculate the remainder
    total_remainder = total_budget - total_expenses

    data = {
        'totalBudget': total_budget,
        'totalExpenses': total_expenses,
        'totalRemainder': total_remainder
    }
    return jsonify(data)


@app.route('/get-in-progress-spending', methods=['POST'])
def get_in_progress_spending():
    data = request.get_json()
    start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
    category_id = data.get('categoryId')

    spending_data = calculate_in_progress_spending(start_date, end_date, category_id)
    return jsonify(spending_data)

@app.route('/get-forecast-spending', methods=['POST'])
def get_forecast_spending():
    data = request.get_json()
    start_date = datetime.strptime(data['startDate'], '%Y-%m-%d')
    end_date = datetime.strptime(data['endDate'], '%Y-%m-%d')
    category_id = data.get('categoryId')

    # Fetch past spending data for the forecasting
    past_spending_query = db.session.query(
        Expense.date, func.sum(Expense.amount).label('amount')
    ).group_by(Expense.date)

    if category_id is not None:
        past_spending_query = past_spending_query.filter(Expense.category_id == category_id)

    past_spending = past_spending_query.all()
    past_dates = [record.date for record in past_spending]
    past_values = [float(record.amount) for record in past_spending]
    
    # Calculate the average daily spend
    if past_dates:
        total_days = (max(past_dates) - min(past_dates)).days + 1
        average_daily_spend = sum(past_values) / total_days
    else:
        average_daily_spend = 0

    # Forecast future spending based on average daily spend
    forecast_spending = []
    for i in range((end_date - start_date).days + 1):
        forecast_date = start_date + timedelta(days=i)
        forecast_spending.append({
            'date': forecast_date.strftime('%Y-%m-%d'),
            'total': average_daily_spend  # Simple forecast based on average daily spend
        })

    labels = [item['date'] for item in forecast_spending]
    values = [item['total'] for item in forecast_spending]

    return jsonify({'labels': labels, 'values': values})


def calculate_in_progress_spending(start_date, end_date, category_id):
    query = db.session.query(
        Expense.date, func.sum(Expense.amount).label('total')
    ).group_by(Expense.date)

    if category_id is not None:
        query = query.filter(Expense.category_id == category_id)

    in_progress_spending = query.filter(
        Expense.date >= start_date, 
        Expense.date <= end_date
    ).all()

    labels = [result.date.strftime('%Y-%m-%d') for result in in_progress_spending]
    values = [result.total for result in in_progress_spending]

    return {'labels': labels, 'values': values}

def calculate_forecast_spending(start_date, end_date, category_id):
    # Replace this part with your actual forecast logic
    forecast_spending = [
        {'date': start_date, 'total': 100},
        {'date': end_date, 'total': 150}
    ]

    labels = [item['date'].strftime('%Y-%m-%d') for item in forecast_spending]
    values = [item['total'] for item in forecast_spending]

    return {'labels': labels, 'values': values}


@app.route('/get-date-range-data', methods=['GET'])
def get_date_range_data():
    from_date = request.args.get('from')
    to_date = request.args.get('to')
    category_id = request.args.get('categoryId', default=None, type=int)

    try:
        from_date = datetime.strptime(from_date, '%Y-%m-%d')
        to_date = datetime.strptime(to_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    in_progress_spending_query = db.session.query(
        Expense.date, func.sum(Expense.amount).label('amount')
    ).filter(
        Expense.date >= from_date,
        Expense.date <= to_date
    )

    # Apply category filter if provided
    if category_id is not None:
        in_progress_spending_query = in_progress_spending_query.filter(Expense.category_id == category_id)

    in_progress_spending_query = in_progress_spending_query.group_by(Expense.date).all()

    in_progress_data = {
        'labels': [record.date.strftime('%Y-%m-%d') for record in in_progress_spending_query],
        'values': [float(record.amount) for record in in_progress_spending_query]
    }

    # Implement your forecast logic here and populate forecast_data accordingly
    forecast_data = {
        'labels': [(from_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((to_date - from_date).days + 1)],
        'values': [0 for _ in range((to_date - from_date).days + 1)]  # Replace 0 with actual forecasted values
    }

    combined_data = {
        'inProgressSpending': in_progress_data,
        'forecastSpending': forecast_data
    }

    return jsonify(combined_data)
