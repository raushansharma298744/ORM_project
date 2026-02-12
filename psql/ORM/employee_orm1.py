from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Column,String,Integer

#step 1 connecte engine with database
engine=create_engine("sqlite:////hello.db")

#step 2 cerate base declaerative
base=declarative_base()

#step 3 create orm class
class Employee(base):
    __tablename__="hyy"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    gender=Column(String)

#step 4 create table
base.metadata.create_all(engine)

#step 5 session create

Session=sessionmaker(bind=engine)
session=Session()
session.query(Employee).delete()
session.commit()

#step7  insert data into table
r1=Employee(name="raushan",age=21,gender='M')
r2=Employee(name="sameer",age=22,gender='M')
r3=Employee(name="radhikar",age=23,gender='F')

session.add_all([r1,r2,r3])
session.commit()

employees=session.query(Employee).all()
for i in employees:
    print(i.name,i.age,i.gender)


