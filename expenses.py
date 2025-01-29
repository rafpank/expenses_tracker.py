# $ python /expenses.py add 100 "Shopping for one hundred zloty"
# $ python /expenses.py add 5000 "Large expense"
# $ python /expenses.py add 25.5 "Shopping for 25.50"
# $ python /expenses.py add -- -100 "Negative expense"
# $ python /expenses.py report
# $ python /expenses.py report --big
# $ python /expenses.py import-python
# $ python /expenses.py export-csv
# $ python /expenses.py export-python

from dataclasses import dataclass
from typing import List, Union
import csv
import pickle

import click

DB_FILENAME = 'expenses.db'
CSV_TO_IMPORT = 'expenses.csv'
CSV_TO_EXPORT = 'expenses1.csv'

@dataclass
class Expense:
    id: int
    description: str
    value: float
    pricey: bool

    def __post_init__(self):
        if not self.description:
            raise ValueError('Description is required.')

def find_next_id(expenses: List[Expense]):
    ids = {expense.id for expense in expenses}
    counter = 1
    while counter in ids:
        counter += 1
    return counter

def read_db_or_init() -> List[Expense]:
    try:
        with open(DB_FILENAME, 'rb') as stream:
            expenses = pickle.load(stream)
    except (FileNotFoundError, EOFError):
        expenses = []
    return expenses

def import_csv() -> List[Expense]:
    try:
        with open(CSV_TO_IMPORT, 'r', encoding='utf-8') as stream:
            reader = csv.reader(stream)
            next(reader)  # Skip the header
            existing_expenses = read_db_or_init()  # Load the existing database
            expenses = []

            for row in reader:
                try:
                    value = float(row[0])  # Value as a float
                    description = row[1].strip()  # Description
                    if not description:
                        raise ValueError("Missing description in the row.")

                    # Generate a new id based on the existing database
                    new_id = find_next_id(existing_expenses + expenses)

                    # Create an Expense object
                    expenses.append(Expense(
                        id=new_id,
                        value=value,
                        pricey=value >= 1000,
                        description=description
                    ))

                except (ValueError, IndexError) as e:
                    print(f"Error in row {row}: {e}")

    except FileNotFoundError:
        print("CSV file not found.")
        expenses = []

    return expenses

def save_db(expenses: List[Expense]) -> None:
    with open(DB_FILENAME, 'wb') as stream:
        pickle.dump(expenses, stream)

def save_to_csv(expenses: List[Expense]) -> None:
    try:
        with open(CSV_TO_EXPORT, 'w', encoding='utf-8') as stream:
            writer = csv.writer(stream)
            writer.writerow(['id', 'amount', 'description', 'big'])
            for expense in expenses:
                writer.writerow([expense.id, expense.value, expense.description, expense.pricey])
    except FileNotFoundError:
        print('File not found.')

def print_expenses(expenses: List[Expense]) -> None:
    print(f"--ID-- -AMOUNT- -BIG?- --DESCRIPTION-------------")
    total = 0
    for expense in expenses:
        big = '(!)' if expense.pricey else ''
        print(f'{expense.id:^6} {expense.value:>8.2f} {big:^6} {expense.description}')
        total += expense.value
    
    print('Total expenses:', total)

def add_expense(value: float, description: str, expenses: List[Expense]) -> None:
    if value <= 0:
        raise ValueError('The amount must be positive.')
    expense = Expense(
        id=find_next_id(expenses),
        value=value,
        pricey=value >= 1000,
        description=description,
    )
    expenses.append(expense)

def validate_description_or_value(item: Union[str, float]):
    if isinstance(item, (int, float)):
        if item <= 0:
            raise ValueError("The amount must be positive.")
    elif isinstance(item, str):
        if not item.strip():
            raise ValueError("Description cannot be empty.")
    else:
        raise TypeError("Invalid type.")

@click.group()
def cli():
    pass

@cli.command()
@click.option('--big', is_flag=True, help='Display only large expenses (above 1000).')
def report(big: bool) -> None:
    expenses = read_db_or_init()
    if big:
        expenses = [expense for expense in expenses if expense.pricey]
    print_expenses(expenses)

@cli.command()
@click.argument('value', type=float)
@click.argument('description', type=str)
def add(value: float, description: str):
    try:
        validate_description_or_value(value)
        validate_description_or_value(description)
    except ValueError as e:
        print(f"Error: {e}")
        return
    expenses = read_db_or_init()
    add_expense(value, description, expenses)
    save_db(expenses)
    print('Expense added!')

@cli.command()
def export_python():
    expenses = read_db_or_init()
    print(expenses)

@cli.command()
def export_csv():
    expenses = read_db_or_init()
    print_expenses(expenses)
    save_to_csv(expenses)
    print('Expenses have been saved to a CSV file.')

@cli.command()
def import_python():
    imported_expenses = import_csv()
    if not imported_expenses:
        print("No data to import.")
        return

    print("Imported expenses:")
    print_expenses(imported_expenses)
    choice = input('Append imported expenses to the existing database? [y/n] ').lower()
    if choice == 'y':
        existing_expenses = read_db_or_init()
        merged_expenses = existing_expenses + imported_expenses
        save_db(merged_expenses)
        print('Imported data from the CSV file has been added to the database.')
    elif choice == 'n':
        print('Import canceled.')
    else:
        print('Invalid choice. Import canceled.')

if __name__ == '__main__':
    cli()
