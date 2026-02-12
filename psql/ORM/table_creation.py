#import create_engine ot connect the database
from sqlalchemy import create_engine

#sql lite database
# file name is school_db
#will be created if not exist

#STEP 1
engine=create_engine("sqlite:////school_db")  #school_db is file name
print("database connected")



from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker   #used to import values
#create base class

#STEP 2
Base=declarative_base()
#base will be parent of all models

#STEP 3
class Student(Base):
    __tablename__="students"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    course=Column(String)
#create all table defined using base

#STEP 4
Base.metadata.create_all(engine)

#STEP 5
Session=sessionmaker(bind=engine) #
session=Session()
s1=Student(name="Raushan",age=20,course="python")
s2=Student(name="karan",age=22,course="java")
session.add_all([s1, s2])
session.commit()
students=session.query(Student).all()
for i in students:
    print(i.name,i.course)
