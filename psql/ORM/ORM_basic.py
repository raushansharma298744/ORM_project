#import create_engine ot connect the database
from sqlalchemy import create_engine
from sqlalchemy import inspect
#sql lite database
# file name is school_db
#will be created if not exist

engine = create_engine(
    "mysql+pymysql://username:password@localhost:3306/school1"
)
print("database connected")
inspector=inspect(engine)
tables=inspector.get_table_names()
print(tables)
