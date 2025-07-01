import sqlite3
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, 'archivesmotott.db')
ddl_script_path = os.path.join(current_dir, 'schema.sql')
dml_script_path = os.path.join(current_dir, 'datas.sql')

try:
    connection = sqlite3.connect(db_path)

    # DDL
    with open(ddl_script_path, 'r') as f:
        connection.executescript(f.read())
    print("#######################")
    print("DDL DB OK")


    # DML
    with open(dml_script_path, 'r') as f:
        connection.executescript(f.read())
    print("#######################")
    print("DML DB OK")

except Exception as e:
    print("#######################")
    print("init DB KO") 
    print(f"Erreur : {e}")
finally:
    connection.commit()
    connection.close()