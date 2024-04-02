import sqlite3
import json

def generate_schema_files(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query to get all table names in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    table_dict = {}
    column_dict = {}
    
    for (table,) in tables:
        # Query to get all column names for each table
        cursor.execute(f"PRAGMA table_info({table});")
        columns = cursor.fetchall()
        
        # Update table dictionary
        table_dict[table] = [column[1] for column in columns]  # column[1] contains the column name
        
        # Update column dictionary
        for column in columns:
            column_name = column[1]
            if column_name not in column_dict:
                column_dict[column_name] = [table]
            else:
                column_dict[column_name].append(table)
    
    # Close the database connection
    conn.close()
    
    # Write dictionaries to JSON files
    with open('table_dictionary.json', 'w') as f:
        json.dump(table_dict, f, indent=4)
    
    with open('column_dictionary.json', 'w') as f:
        json.dump(column_dict, f, indent=4)
        
    print("Schema files generated successfully.")

# Example usage
db_path = 'your_database_path_here.db'
generate_schema_files(db_path)
