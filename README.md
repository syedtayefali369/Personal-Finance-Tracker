# Personal-Finance-Tracker
A command-line program where users can add expenses/income, categorize them, save data, analyze spending, and generate simple reports.

This one project naturally uses:
✔ Variables & data types
✔ Input/output
✔ Conditions & loops
✔ Functions
✔ Lists, dicts, tuples
✔ File handling (JSON/CSV)
✔ Error handling
✔ Modules
✔ OOP (optional but recommended)
✔ Date/time
✔ Basic algorithms (sorting, filtering)
✔ Intermediate concepts (classes, imports, comprehension, exceptions)

🧱 Features to Include
1. Add Transaction (Expense/Income)

Ask user for:

amount

type (expense/income)

category (food, travel, salary…)

date

notes

Store in list/dictionary.

2. Save & Load Data

Save data in a JSON file.

Load it automatically when program starts.

3. View All Transactions

Display records in a table style text format.

Use sorting (by date, amount, category).

4. Filter Transactions

Filter by:

date range

category

expense-only or income-only

5. Summary Report

Compute:

total expenses

total income

balance

category-wise breakdown

Use dictionary + loops.

6. Error Handling

Examples:

try:
    amount = float(input("Enter amount: "))
except ValueError:
    print("Invalid amount!")

7. Optional Intermediate Add-ons

Create a Transaction class (OOP).

Create a separate module: utils.py for helper functions.

Generate plots using matplotlib.

Export a CSV file.

Add password login (simple hashing).

Use argparse to execute commands directly.

🧩 Project Structure (Simple)
finance_tracker/
│
├── main.py
├── data.json
├── utils.py
└── models.py   (optional, for OOP)
