"""
Utility functions for Finance Tracker
Helper functions for data validation, formatting, and analysis
"""

import re
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np

def validate_amount(amount_str):
    """
    Validate if the input is a positive number
    Returns float if valid, None if invalid
    """
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None
        return amount
    except ValueError:
        return None

def validate_date(date_str):
    """
    Validate date format (YYYY-MM-DD)
    Returns formatted date if valid, None if invalid
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None

def format_currency(amount):
    """Format amount as currency string"""
    return f"${amount:,.2f}"

def calculate_category_totals(transactions):
    """Calculate total amounts for each category"""
    category_totals = {}
    for transaction in transactions:
        if transaction.category not in category_totals:
            category_totals[transaction.category] = 0
        if transaction.transaction_type == 'income':
            category_totals[transaction.category] += transaction.amount
        else:
            category_totals[transaction.category] -= transaction.amount
    
    return category_totals

def generate_spending_report(transactions, days=30):
    """Generate a spending report for the last N days"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    recent_transactions = [
        t for t in transactions 
        if start_date <= datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S") <= end_date
    ]
    
    expenses = [t for t in recent_transactions if t.transaction_type == 'expense']
    income = [t for t in recent_transactions if t.transaction_type == 'income']
    
    report = {
        'period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'total_income': sum(t.amount for t in income),
        'total_expenses': sum(t.amount for t in expenses),
        'net_balance': sum(t.amount for t in income) - sum(t.amount for t in expenses),
        'expense_by_category': {},
        'income_by_category': {}
    }
    
    for expense in expenses:
        if expense.category not in report['expense_by_category']:
            report['expense_by_category'][expense.category] = 0
        report['expense_by_category'][expense.category] += expense.amount
    
    for inc in income:
        if inc.category not in report['income_by_category']:
            report['income_by_category'][inc.category] = 0
        report['income_by_category'][inc.category] += inc.amount
    
    return report

def plot_spending_by_category(transactions, transaction_type='expense'):
    """Create a pie chart of spending/income by category"""
    if transaction_type not in ['income', 'expense']:
        raise ValueError("Transaction type must be 'income' or 'expense'")
    
    category_totals = {}
    for transaction in transactions:
        if transaction.transaction_type == transaction_type:
            if transaction.category not in category_totals:
                category_totals[transaction.category] = 0
            category_totals[transaction.category] += transaction.amount
    
    if not category_totals:
        print(f"No {transaction_type} data to display.")
        return
    
    # Prepare data for plotting
    categories = list(category_totals.keys())
    amounts = list(category_totals.values())
    
    plt.figure(figsize=(10, 8))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
    plt.title(f'{transaction_type.title()} by Category')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def plot_income_vs_expenses(transactions, months=6):
    """Create a bar chart comparing income vs expenses over time"""
    current_date = datetime.now()
    monthly_data = []
    
    for i in range(months-1, -1, -1):
        target_date = current_date - timedelta(days=30*i)
        year = target_date.year
        month = target_date.month
        
        monthly_transactions = [
            t for t in transactions 
            if datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").year == year and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").month == month
        ]
        
        income = sum(t.amount for t in monthly_transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense')
        
        monthly_data.append({
            'month': target_date.strftime('%Y-%m'),
            'income': income,
            'expenses': expenses
        })
    
    months_list = [data['month'] for data in monthly_data]
    income_list = [data['income'] for data in monthly_data]
    expenses_list = [data['expenses'] for data in monthly_data]
    
    x = np.arange(len(months_list))
    width = 0.35
    
    plt.figure(figsize=(12, 6))
    plt.bar(x - width/2, income_list, width, label='Income', color='green', alpha=0.7)
    plt.bar(x + width/2, expenses_list, width, label='Expenses', color='red', alpha=0.7)
    
    plt.xlabel('Month')
    plt.ylabel('Amount ($)')
    plt.title('Income vs Expenses Over Time')
    plt.xticks(x, months_list, rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

def input_with_validation(prompt, validation_func, error_message="Invalid input. Please try again."):
    """Get validated input from user"""
    while True:
        user_input = input(prompt).strip()
        validated_input = validation_func(user_input)
        if validated_input is not None:
            return validated_input
        print(error_message)