# expenses_tracker.py
Expenses tracker

# command line commands
 $ python /expenses.py add 100 "Shopping for one hundred"
 $ python /expenses.py add 25.5 "Shopping for 25.50"
 $ python /expenses.py add 5000 "Large expense"
 $ python /expenses.py add -- -100 "Negative expense"
 $ python /expenses.py report
 $ python /expenses.py report --big
 $ python /expenses.py import-python
 $ python /expenses.py export-csv
 $ python /expenses.py export-python

The program enables users to easily add new expenses and generate reports. It retains data between sessions by storing all information in a file. Each expense has an ID, a description, and an amount.

The program includes subcommands: add, report, report --big, export-python, export-csv and import-csv.

The add subcommand allows for adding a new expense. Users need to provide the expense amount and its description (in quotes) as command-line arguments. For instance:
$ python budget.py add 100 "shopping for a hundred zloty".
The ID assigned is the first available ID—e.g., if expenses with IDs 1, 2, 4, and 5 already exist, the next ID should be 3.

The report subcommand displays all expenses in a table format. The table includes a "big?" column, which shows a checkmark if the expense is substantial (i.e., at least 1000). Additionally, the total sum of all expenses is displayed at the end.

The export-python subcommand shows the list of all expenses as an object.

The import-csv subcommand imports a list of expenses from a CSV file.

The program stores all expenses between sessions in the expenses.db file.  If the file does not exist, a new, empty database is automatically created. .

The expense amount must be a positive number. 
