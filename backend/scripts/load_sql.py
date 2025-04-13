import os
import sys

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.db import db
from flask import Flask


def execute_sql_file(file_path):
    with open(file_path, 'r') as file:
        sql_commands = file.read()

    conn = db.engine.raw_connection()
    cursor = conn.cursor()
    for command in sql_commands.split(';'):
        if command.strip():
            try:
                cursor.execute(command)
            except Exception as e:
                print(f"Erreur : {e}")
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:root@localhost/brique_buster'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        base_dir = os.path.join(os.path.dirname(__file__), '../sql')

        for file_name in ['triggers.sql', 'functions.sql', 'procedures.sql']:
            file_path = os.path.join(base_dir, file_name)
            execute_sql_file(file_path)
            print(f"{file_name} chargé avec succès !")
