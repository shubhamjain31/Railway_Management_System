import sqlite3 
from decouple import config

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

# add_column("rms.db", "users", "is_staff", "Boolean")
# add_column("rms.db", "users", "is_verified", "Boolean")


from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime
engine = create_engine(config("SQLALCHEMY_URL"), echo = True)

# meta = MetaData()

# students = Table(
#    'payments', meta, 
#    Column('id', Integer, primary_key = True), 
#    Column('pnr', String), 
#    Column('email', String), 
#    Column('amt', Integer), 
#    Column('name', String), 
#    Column('date', DateTime), 
#    Column('cancel', String), 
# )

# meta.create_all(engine)

from sqlalchemy.dialects.postgresql import JSON
def add_column(engine, table_name, column):
    column_name = column.compile(dialect=engine.dialect)
    column_type = column.type.compile(engine.dialect)
    engine.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table_name, column_name, column_type))

column = Column('response', JSON)
add_column(engine, 'payments', column)