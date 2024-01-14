import argparse
from db import create_tables
from app import run

parser = argparse.ArgumentParser(description='CLI to setup API.')
subparsers = parser.add_subparsers()

db_parser = subparsers.add_parser('create-tables', help="Creates the tables in the «myapp» database for the project")
db_parser.set_defaults(func=create_tables)

start_parser = subparsers.add_parser('start', help="Starts the API")
start_parser.set_defaults(func=run)

# Write 'python main.py create-tables' or 'python main.py start' in the console
if __name__ == '__main__':
    args = parser.parse_args()
    args.func()
