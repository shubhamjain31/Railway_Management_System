import sqlite3 

def add_column(database_name, table_name, column_name, data_type):

    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    if data_type == "Integer":
        data_type_formatted = "INTEGER"
    elif data_type == "String":
        data_type_formatted = "VARCHAR(100)"
    elif data_type == "Boolean":
        data_type_formatted = "Boolean"


    base_command = ("ALTER TABLE '{table_name}' ADD column '{column_name}' '{data_type}'")
    sql_command = base_command.format(table_name=table_name, column_name=column_name, data_type=data_type_formatted)

    cursor.execute(sql_command)
    connection.commit()
    connection.close()

add_column("rms.db", "users", "is_staff", "Boolean")
add_column("rms.db", "users", "is_verified", "Boolean")