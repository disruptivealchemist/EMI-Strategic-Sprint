import sqlite3
import csv
import json
import os

# Paths to input files
BRAND_ASSETS_CSV = '/Users/lisag/Documents/04 Development/Clients/EMI-Emery/ARCHIVE-PHASE1-RESEARCH/brand-assets/EMERY Brand Assets 2aaa930f46b480b49bf6f3161311ebc9.csv'
TASKS_EXPORT_CSV = '/Users/lisag/Documents/04 Development/Clients/EMI-Emery/CURRENT-PROJECT-PHASE2/EMI-TASKS-EXPORT.csv'
DB_PATH = '/Users/lisag/Documents/04 Development/Clients/EMI-Emery/CURRENT-PROJECT-PHASE2/project_assets.db'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)

def insert_data(conn, table, data):
    """ insert data into table
    """
    if not data:
        return
    
    keys = data[0].keys()
    columns = ', '.join(keys)
    placeholders = ', '.join('?' * len(keys))
    sql = f''' INSERT INTO {table}({columns}) VALUES({placeholders}) '''
    
    cur = conn.cursor()
    for row in data:
        cur.execute(sql, list(row.values()))
    conn.commit()

def csv_to_dict_list(csv_file):
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)

def main():
    # Remove existing db if it exists to start fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = create_connection(DB_PATH)

    if conn is not None:
        # 1. Process Brand Assets
        print("Processing Brand Assets...")
        brand_assets = csv_to_dict_list(BRAND_ASSETS_CSV)
        if brand_assets:
            # Generate CREATE TABLE statement dynamically based on CSV columns
            columns = brand_assets[0].keys()
            # Sanitize column names for SQL
            sanitized_columns = [c.replace(' ', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '') for c in columns]
            
            # Remap keys in data to sanitized column names
            sanitized_brand_assets = []
            for row in brand_assets:
                new_row = {}
                for k, v in row.items():
                   sanitized_key = k.replace(' ', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '')
                   new_row[sanitized_key] = v
                sanitized_brand_assets.append(new_row)

            
            create_table_sql = f""" CREATE TABLE IF NOT EXISTS existing_assets (
                                        id INTEGER PRIMARY KEY,
                                        {', '.join([f'"{c}" TEXT' for c in sanitized_columns])}
                                    ); """
            create_table(conn, create_table_sql)
            insert_data(conn, "existing_assets", sanitized_brand_assets)
            print(f"Inserted {len(sanitized_brand_assets)} existing assets.")

        # 2. Process Requested Assets (Tasks)
        print("Processing Requested Assets...")
        tasks = csv_to_dict_list(TASKS_EXPORT_CSV)
        if tasks:
             # Generate CREATE TABLE statement dynamically
            columns = tasks[0].keys()
            # Sanitize column names for SQL
            sanitized_columns = [c.replace(' ', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '') for c in columns]
             
             # Remap keys in data to sanitized column names
            sanitized_tasks = []
            for row in tasks:
                new_row = {}
                for k, v in row.items():
                   sanitized_key = k.replace(' ', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '')
                   new_row[sanitized_key] = v
                sanitized_tasks.append(new_row)


            create_table_sql = f""" CREATE TABLE IF NOT EXISTS requested_assets (
                                        id INTEGER PRIMARY KEY,
                                        {', '.join([f'"{c}" TEXT' for c in sanitized_columns])}
                                    ); """
            create_table(conn, create_table_sql)
            insert_data(conn, "requested_assets", sanitized_tasks)
            print(f"Inserted {len(sanitized_tasks)} requested assets.")
        
        # 3. Create a unified view
        print("Creating Unified View...")
        create_view_sql = """
        CREATE VIEW all_assets_unified AS
        SELECT 
            Asset_Name as name,
            Description as description,
            Asset_Type as type_category,
            Status as status,
            'Existing' as origin_source,
            Link as link_or_deadline
        FROM existing_assets
        UNION ALL
        SELECT 
            Task_Name as name,
            Description_Notes as description,
            Category as type_category,
            Status as status,
            'Requested' as origin_source,
            Deadline as link_or_deadline
        FROM requested_assets;
        """
        try:
            c = conn.cursor()
            c.execute(create_view_sql)
            print("Unified view created.")
        except sqlite3.Error as e:
            print(f"Error creating view: {e}")

        conn.close()
        print(f"Database created successfully at: {DB_PATH}")
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()
