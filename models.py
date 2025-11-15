"""
Models for Finance Tracker
Contains classes for financial transactions and categories
"""

from datetime import datetime
import json

class Transaction:
    """Represents a financial transaction"""
    
    def __init__(self, amount, category, transaction_type, description="", date=None):
        self.amount = float(amount)
        self.category = category
        self.transaction_type = transaction_type  # 'income' or 'expense'
        self.description = description
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.id = self._generate_id()
    
    def _generate_id(self):
        """Generate a unique ID for the transaction"""
        return f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{hash(self.description) % 10000}"
    
    def to_dict(self):
        """Convert transaction to dictionary for JSON storage"""
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'type': self.transaction_type,
            'description': self.description,
            'date': self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Transaction object from dictionary"""
        transaction = cls(
            amount=data['amount'],
            category=data['category'],
            transaction_type=data['type'],
            description=data['description'],
            date=data['date']
        )
        transaction.id = data['id']
        return transaction
    
    def __str__(self):
        return f"{self.date} - {self.transaction_type.upper()}: ${self.amount:.2f} - {self.category}"

class FinanceTracker:
    """Main class to manage financial transactions"""
    
    def __init__(self, data_file="data.json"):
        self.data_file = data_file
        self.transactions = []
        self.categories = {
            'income': ['Salary', 'Freelance', 'Investment', 'Gift', 'Other'],
            'expense': ['Food', 'Transport', 'Entertainment', 'Bills', 'Shopping', 'Healthcare', 'Other']
        }
        self.load_data()
    
    def add_transaction(self, amount, category, transaction_type, description=""):
        """Add a new transaction"""
        if transaction_type not in ['income', 'expense']:
            raise ValueError("Transaction type must be 'income' or 'expense'")
        
        if category not in self.categories[transaction_type]:
            # Add new category if it doesn't exist
            self.categories[transaction_type].append(category)
        
        transaction = Transaction(amount, category, transaction_type, description)
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_balance(self):
        """Calculate current balance"""
        income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return income - expenses
    
    def get_transactions_by_type(self, transaction_type):
        """Get all transactions of a specific type"""
        return [t for t in self.transactions if t.transaction_type == transaction_type]
    
    def get_transactions_by_category(self, category):
        """Get all transactions in a specific category"""
        return [t for t in self.transactions if t.category == category]
    
    def get_monthly_summary(self, year=None, month=None):
        """Get monthly summary of income and expenses"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        monthly_transactions = [
            t for t in self.transactions 
            if datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").year == year and
            datetime.strptime(t.date, "%Y-%m-%d %H:%M:%S").month == month
        ]
        
        income = sum(t.amount for t in monthly_transactions if t.transaction_type == 'income')
        expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense')
        
        return {
            'income': income,
            'expenses': expenses,
            'balance': income - expenses,
            'transaction_count': len(monthly_transactions)
        }
    
    def delete_transaction(self, transaction_id):
        """Delete a transaction by ID"""
        self.transactions = [t for t in self.transactions if t.id != transaction_id]
        self.save_data()
        return True
    
    def load_data(self):
        """Load transactions from JSON file"""
        try:
            with open(self.data_file, 'r') as file:
                data = json.load(file)
                self.transactions = [Transaction.from_dict(t) for t in data.get('transactions', [])]
                self.categories = data.get('categories', self.categories)
        except FileNotFoundError:
            # Initialize with empty data if file doesn't exist
            self.transactions = []
            self.categories = self.categories
    
    def save_data(self):
        """Save transactions to JSON file"""
        data = {
            'transactions': [t.to_dict() for t in self.transactions],
            'categories': self.categories
        }
        with open(self.data_file, 'w') as file:
            json.dump(data, file, indent=2)