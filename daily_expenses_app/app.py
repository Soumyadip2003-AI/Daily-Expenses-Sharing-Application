from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
import io

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(15), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

    user = db.relationship('User', backref=db.backref('expenses', lazy=True))

class SplitExpense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expense_id = db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    split_amount = db.Column(db.Float, nullable=False)

    expense = db.relationship('Expense', backref=db.backref('split_expenses', lazy=True))
    user = db.relationship('User', backref=db.backref('split_expenses', lazy=True))

with app.app_context():
    db.create_all()

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], mobile=data['mobile'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

@app.route('/expense', methods=['POST'])
def add_expense():
    data = request.get_json()
    new_expense = Expense(user_id=data['user_id'], amount=data['amount'], description=data.get('description'))
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Expense added successfully!"}), 201


@app.route('/split_expense', methods=['POST'])
def split_expense():
    data = request.get_json()
    expense_id = data['expense_id']
    split_type = data['split_type']
    participants = data['participants']  

    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"message": "Expense not found!"}), 404

    total_amount = expense.amount
    
    if split_type == 'equal':
     
        amount_per_user = total_amount / len(participants)
        for user_id in participants:
            new_split = SplitExpense(expense_id=expense_id, user_id=user_id, split_amount=amount_per_user)
            db.session.add(new_split)

    elif split_type == 'exact':
        
        for participant in participants:
            user_id = participant['user_id']
            amount = participant['amount']
            new_split = SplitExpense(expense_id=expense_id, user_id=user_id, split_amount=amount)
            db.session.add(new_split)

    elif split_type == 'percentage':
        
        total_percentage = sum([p['percentage'] for p in participants])
        if total_percentage != 100:
            return jsonify({"message": "Percentages must add up to 100!"}), 400

        for participant in participants:
            user_id = participant['user_id']
            percentage = participant['percentage']
            amount = total_amount * (percentage / 100)
            new_split = SplitExpense(expense_id=expense_id, user_id=user_id, split_amount=amount)
            db.session.add(new_split)

    db.session.commit()
    return jsonify({"message": "Expense split successfully!"}), 201

@app.route('/expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([{"id": exp.id, "user_id": exp.user_id, "amount": exp.amount, "description": exp.description} for exp in expenses])

@app.route('/total_expense', methods=['GET'])
def total_expense():
    total = db.session.query(func.sum(Expense.amount)).scalar()
    return jsonify({"total_expense": total if total else 0})

@app.route('/delete_expense/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if not expense:
        return jsonify({"message": "Expense not found!"}), 404
    db.session.delete(expense)
    db.session.commit()
    return jsonify({"message": "Expense deleted successfully!"}), 200

@app.route('/download_expenses', methods=['GET'])
def download_expenses():
    expenses = Expense.query.all()
    data = [{"ID": exp.id, "User ID": exp.user_id, "Amount": exp.amount, "Description": exp.description} for exp in expenses]
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Expenses')
    output.seek(0)
    return Response(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    headers={"Content-Disposition": "attachment;filename=expenses.xlsx"})

@app.route('/')
def welcome():
    return "Welcome to the Daily Expenses API!"

if __name__ == '__main__':
    app.run(debug=True)
