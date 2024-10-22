This is a Flask-based API for managing users and expenses. The API allows for creating users, adding expenses, splitting expenses among participants using different methods (Equal, Exact, and Percentage), and downloading an Excel balance sheet.
Setup and Installation:-
---------------------------
1. Clone the repository.
2. Install the required packages(pip install -r requirements.txt).
3. Run the application.

User Endpoints:-
-------------------------
create user database:-
---------------------------
url:http://127.0.0.1:5000/Create user (**method should be post**).

Retrieve User Details
--------------------------
url:http://127.0.0.1:5000/expense/user_id (**method should be post**).

Add Expense:-
--------------------------
url:http://127.0.0.1:5000/expense (**method should be post**).

Retrieve Individual User Expenses:-
-------------------------------------
url:http://127.0.0.1:5000/user_expenses/1 (**method should be get**).

Get Total Expenses:-
----------------------------------
url:http://127.0.0.1:5000/total_expense (**method should be get**)

Download Balance Sheet:-
-----------------------------------
url:http://127.0.0.1:5000/download_expenses(**method should be get**).

Split an Expense (Equal):-
--------------------------------------
url:http://127.0.0.1:5000/split_expense(**method should be get**).

Split an Expense (Exact):-
--------------------------------------
url:http://127.0.0.1:5000/split_expense(**method should be get**).

Split an Expense (Percentage):-
---------------------------------
url:http://127.0.0.1:5000/split_expense(**method should be get**).

Instructions:
------------------
**Body: For POST requests, select "raw" and set the type to JSON.**




