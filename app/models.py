from app import db
from datetime import datetime

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(80), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(120), nullable=False)  # Name of the expense
    currency = db.Column(db.String(10), nullable=True)  # Currency (you might want to set a default value)
    recurring = db.Column(db.String(5), nullable=True)  # 'Yes' or 'No' for recurring
    

    def __repr__(self):
        return f"Expense('{self.category}', '{self.amount}', '{self.date}')"
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    priority = db.Column(db.Integer, nullable=True)

Category.serialize = property(lambda self: {
    "id": self.id,
    "name": self.name,
    "budget": self.budget,
    "priority": self.priority
})