import shelve
from models import EventStats, Event

def store_in_shelve(table_name, key, obj):
    with shelve.open('csci262asgn3',writeback=True) as db:
        if table_name not in db:
            db[table_name] = {}
        db[table_name][key] = obj

def get_from_shelve(table_name, key):
    with shelve.open('csci262asgn3') as db:
        return db[table_name][key]

def reset_shelve():
    db_name = 'csci262asgn3'
    with shelve.open(db_name,writeback=True) as db:
        db.clear()

def print_shelve_contents():
    db_name = 'csci262asgn3'
    with shelve.open(db_name) as db:
        for table_name in db:
            print(f"Table: {table_name}")
            for key in db[table_name]:
                print(f"  {key}: {db[table_name][key]}")

def export_shelve_contents():
    db_name = 'csci262asgn3'
    with shelve.open(db_name) as db:
        for table_name in db:
            with open(f'./exports/{table_name}_data.txt','w') as file:
                file.write(f"{len(db[table_name])}\n")
                for key in db[table_name]:
                    file.write(f"{db[table_name][key]}\n")
def export_shelve_table(table_name):
    db_name = 'csci262asgn3'
    with shelve.open(db_name) as db:
        with open(f'./exports/{table_name}_data.txt','w') as file:
            file.write(f"{len(db[table_name])}\n")
            for key in db[table_name]:
                file.write(f"{db[table_name][key]}\n")
    return f'./exports/{table_name}_data.txt'