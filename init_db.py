"""
Database initialisation script
"""

import pymysql
from config import Config

def create_database():
    
    try:
        connection = pymysql.connect(
            host=Config.DB_HOST,
            port=int(Config.DB_PORT),
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{Config.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"Database '{Config.DB_NAME}' created or already exists.")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def create_tables():
    """ Create tables using SQLAlchemy """
    try:
        from app import app
        from models import db
        
        with app.app_context():
            db.create_all()
            print("Tables created successfully.")
        return True
        
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == '__main__':
    print("Initialising database...")
    
    if create_database():
        if create_tables():
            print("Database initialisation completed successfully!")
        else:
            print("Failed to create tables.")
    else:
        print("Failed to create database.")