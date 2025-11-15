#!/usr/bin/env python3
"""
Finance Tracker - Main Application
A comprehensive personal finance tracking system
"""

from models import FinanceTracker, Transaction
from utils import (
    validate_amount, validate_date, format_currency,
    generate_spending_report, plot_spending_by_category,
    plot_income_vs_expenses, input_with_validation
)
import os
from datetime import datetime

class FinanceTrackerApp:
    """Main application class for Finance Tracker"""
    
    def __init__(self):
        self.tracker = FinanceTracker()
        self.running = True
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("          PERSONAL FINANCE TRACKER")
        print("="*50)
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View All Transactions")
        print("4. View Balance")
        print("5. Monthly Summary")
        print("6. Spending Report")
        print("7. View Categories")
        print("8. Data Visualization")
        print("9. Delete Transaction")
        print("0. Exit")
        print("="*50)
    
    def add_income(self):
        """Add an income transaction"""
        print("\n--- Add Income ---")
        
        amount = input_with_validation(
            "Enter amount: $",
            validate_amount,
            "Please enter a valid positive number."
        )
        
        print("\nAvailable categories:")
        for i, category in enumerate(self.tracker.categories['income'], 1):
            print(f"{i}. {category}")
        print(f"{len(self.tracker.categories['income']) + 1}. Add new category")
        
        try:
            choice = int(input("\nSelect category (number): "))
            if 1 <= choice <= len(self.tracker.categories['income']):
                category = self.tracker.categories['income'][choice-1]
            elif choice == len(self.tracker.categories['income']) + 1:
                category = input("Enter new category name: ").strip()
                if not category:
                    print("Category name cannot be empty.")
                    return
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return
        
        description = input("Enter description (optional): ").strip()
        
        transaction = self.tracker.add_transaction(amount, category, 'income', description)
        print(f"\n✓ Income added successfully!")
        print(f"  {transaction}")
    
    def add_expense(self):
        """Add an expense transaction"""
        print("\n--- Add Expense ---")
        
        amount = input_with_validation(
            "Enter amount: $",
            validate_amount,
            "Please enter a valid positive number."
        )
        
        print("\nAvailable categories:")
        for i, category in enumerate(self.tracker.categories['expense'], 1):
            print(f"{i}. {category}")
        print(f"{len(self.tracker.categories['expense']) + 1}. Add new category")
        
        try:
            choice = int(input("\nSelect category (number): "))
            if 1 <= choice <= len(self.tracker.categories['expense']):
                category = self.tracker.categories['expense'][choice-1]
            elif choice == len(self.tracker.categories['expense']) + 1:
                category = input("Enter new category name: ").strip()
                if not category:
                    print("Category name cannot be empty.")
                    return
            else:
                print("Invalid choice.")
                return
        except ValueError:
            print("Please enter a valid number.")
            return
        
        description = input("Enter description (optional): ").strip()
        
        transaction = self.tracker.add_transaction(amount, category, 'expense', description)
        print(f"\n✓ Expense added successfully!")
        print(f"  {transaction}")
    
    def view_transactions(self):
        """Display all transactions"""
        if not self.tracker.transactions:
            print("\nNo transactions found.")
            return
        
        print("\n--- All Transactions ---")
        print(f"{'Date':<20} {'Type':<8} {'Amount':<12} {'Category':<15} {'Description'}")
        print("-" * 80)
        
        for transaction in sorted(self.tracker.transactions, 
                                key=lambda x: datetime.strptime(x.date, "%Y-%m-%d %H:%M:%S"), 
                                reverse=True):
            amount_str = format_currency(transaction.amount)
            type_str = "INCOME" if transaction.transaction_type == 'income' else "EXPENSE"
            date_str = transaction.date[:16]  # Trim seconds for display
            
            print(f"{date_str:<20} {type_str:<8} {amount_str:<12} {transaction.category:<15} {transaction.description}")
    
    def view_balance(self):
        """Display current balance"""
        balance = self.tracker.get_balance()
        total_income = sum(t.amount for t in self.tracker.transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in self.tracker.transactions if t.transaction_type == 'expense')
        
        print("\n--- Financial Summary ---")
        print(f"Total Income:    {format_currency(total_income)}")
        print(f"Total Expenses:  {format_currency(total_expenses)}")
        print(f"Current Balance: {format_currency(balance)}")
        
        if balance > 0:
            print("🎉 Great! You're in positive territory!")
        elif balance < 0:
            print("⚠️  Warning: You're spending more than you earn!")
        else:
            print("⚖️  You're breaking even.")
    
    def monthly_summary(self):
        """Display monthly summary"""
        try:
            year = int(input("Enter year (YYYY) or press Enter for current year: ") or datetime.now().year)
            month = int(input("Enter month (1-12) or press Enter for current month: ") or datetime.now().month)
        except ValueError:
            print("Invalid year or month.")
            return
        
        summary = self.tracker.get_monthly_summary(year, month)
        
        print(f"\n--- Monthly Summary for {month}/{year} ---")
        print(f"Income:    {format_currency(summary['income'])}")
        print(f"Expenses:  {format_currency(summary['expenses'])}")
        print(f"Balance:   {format_currency(summary['balance'])}")
        print(f"Transactions: {summary['transaction_count']}")
    
    def spending_report(self):
        """Generate and display spending report"""
        try:
            days = int(input("Enter number of days for report (default 30): ") or 30)
        except ValueError:
            print("Invalid number of days.")
            return
        
        report = generate_spending_report(self.tracker.transactions, days)
        
        print(f"\n--- Spending Report ({report['period']}) ---")
        print(f"Total Income:    {format_currency(report['total_income'])}")
        print(f"Total Expenses:  {format_currency(report['total_expenses'])}")
        print(f"Net Balance:     {format_currency(report['net_balance'])}")
        
        if report['expense_by_category']:
            print("\nExpenses by Category:")
            for category, amount in sorted(report['expense_by_category'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"  {category}: {format_currency(amount)}")
        
        if report['income_by_category']:
            print("\nIncome by Category:")
            for category, amount in sorted(report['income_by_category'].items(), 
                                         key=lambda x: x[1], reverse=True):
                print(f"  {category}: {format_currency(amount)}")
    
    def view_categories(self):
        """Display all categories"""
        print("\n--- Income Categories ---")
        for category in self.tracker.categories['income']:
            transactions = self.tracker.get_transactions_by_category(category)
            total = sum(t.amount for t in transactions if t.transaction_type == 'income')
            print(f"  {category}: {format_currency(total)}")
        
        print("\n--- Expense Categories ---")
        for category in self.tracker.categories['expense']:
            transactions = self.tracker.get_transactions_by_category(category)
            total = sum(t.amount for t in transactions if t.transaction_type == 'expense')
            print(f"  {category}: {format_currency(total)}")
    
    def data_visualization(self):
        """Display data visualization menu"""
        if not self.tracker.transactions:
            print("\nNo data available for visualization.")
            return
        
        print("\n--- Data Visualization ---")
        print("1. Expense Categories Pie Chart")
        print("2. Income Categories Pie Chart")
        print("3. Income vs Expenses Over Time")
        print("4. Back to Main Menu")
        
        choice = input("Select option: ").strip()
        
        if choice == '1':
            plot_spending_by_category(self.tracker.transactions, 'expense')
        elif choice == '2':
            plot_spending_by_category(self.tracker.transactions, 'income')
        elif choice == '3':
            plot_income_vs_expenses(self.tracker.transactions)
        elif choice == '4':
            return
        else:
            print("Invalid choice.")
    
    def delete_transaction(self):
        """Delete a transaction"""
        if not self.tracker.transactions:
            print("\nNo transactions to delete.")
            return
        
        print("\n--- Delete Transaction ---")
        print("Recent transactions:")
        for i, transaction in enumerate(self.tracker.transactions[-10:], 1):
            print(f"{i}. {transaction}")
        
        try:
            choice = int(input("\nSelect transaction to delete (number): "))
            if 1 <= choice <= len(self.tracker.transactions[-10:]):
                transaction = self.tracker.transactions[-10:][choice-1]
                confirm = input(f"Are you sure you want to delete this transaction? (y/n): ").lower()
                if confirm == 'y':
                    self.tracker.delete_transaction(transaction.id)
                    print("✓ Transaction deleted successfully!")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    def run(self):
        """Main application loop"""
        print("Welcome to Personal Finance Tracker!")
        
        while self.running:
            self.display_menu()
            choice = input("\nSelect an option (0-9): ").strip()
            
            if choice == '1':
                self.add_income()
            elif choice == '2':
                self.add_expense()
            elif choice == '3':
                self.view_transactions()
            elif choice == '4':
                self.view_balance()
            elif choice == '5':
                self.monthly_summary()
            elif choice == '6':
                self.spending_report()
            elif choice == '7':
                self.view_categories()
            elif choice == '8':
                self.data_visualization()
            elif choice == '9':
                self.delete_transaction()
            elif choice == '0':
                self.running = False
                print("\nThank you for using Finance Tracker! Goodbye! 👋")
            else:
                print("Invalid option. Please try again.")
            
            if self.running:
                input("\nPress Enter to continue...")

if __name__ == "__main__":
    app = FinanceTrackerApp()
    app.run()