# ORM ka base system import
from sqlalchemy.orm import declarative_base, sessionmaker

# Table ke columns ke liye
from sqlalchemy import Column, Integer, String, create_engine


# =========================
# STEP 1: Engine create
# =========================
# Engine database aur Python ke beech bridge hai
# sqlite:///company.db → agar file nahi hogi to SQLite khud bana dega
engine = create_engine("sqlite:///company.db")


# =========================
# STEP 2: Declarative Base
# =========================
# Base ek parent class hai
# Jitni bhi ORM classes banengi, sab isi se inherit karengi
Base = declarative_base()


# =========================
# STEP 3: ORM Class (Table)
# =========================
# Ye Python class actual database table ko represent karti hai
class Employee(Base):
    __tablename__ = "employees"   # Table ka naam DB me

    # Column definitions
    id = Column(Integer, primary_key=True)  # auto increment primary key
    name = Column(String)                   # employee ka naam
    age = Column(Integer)                   # age
    department = Column(String)             # department


# =========================
# STEP 4: Table create
# =========================
# Agar table already exist hai → kuch nahi karega
# Agar nahi hai → naya table bana dega
Base.metadata.create_all(engine)


# =========================
# STEP 5: Session create
# =========================
# Session DB ke saath saari baat-cheet karta hai
# INSERT, UPDATE, DELETE sab session ke through hota hai
Session = sessionmaker(bind=engine)
session = Session()


# =========================
# STEP 6: OLD DATA CLEAR
# =========================
# Har run me fresh data chahiye
# Isliye pehle saara purana data delete
session.query(Employee).delete()
session.commit()


# =========================
# STEP 7: INSERT DATA
# =========================
# Employee() → table ka ek row
e1 = Employee(name="Nobita", age=14, department="collector")
e2 = Employee(name="suzuka", age=15, department="IAS")



# add_all ek saath multiple rows insert karta hai
session.add_all([e1, e2])
session.commit()   # yahin actual DB me save hota hai


# =========================
# STEP 8: READ (SELECT *)
# =========================
employees = session.query(Employee).all()   # list of objects

print("\n--- BEFORE UPDATE ---")
for emp in employees:
    print(emp.id, emp.name, emp.age, emp.department)


# =========================
# STEP 9: UPDATE (Nobita → gian)
# =========================
# first() → sirf ek object deta hai
emp = session.query(Employee).filter_by(name="Nobita").first()

if emp:
    emp.name = "gian"    # object ka attribute change
    session.commit()    # commit ke bina update DB me nahi jaata
    print("\nemployee updated")


# =========================
# STEP 10: VERIFY UPDATE
# =========================
employees = session.query(Employee).all()

print("\n--- AFTER UPDATE ---")
for emp in employees:
    print(emp.id, emp.name, emp.age, emp.department)


# =========================
# STEP 11: DELETE (sirf gian)
# =========================
emp = session.query(Employee).filter_by(name="gian").first()

if emp:
    session.delete(emp)   # sirf ek row delete
    session.commit()
    print("\nemployee 'gian' deleted")
else:
    print("\nemployee not found")


# =========================
# STEP 12: FINAL DATA
# =========================
employees = session.query(Employee).all()

print("\n--- FINAL DATA ---")
for emp in employees:
    print(emp.id, emp.name, emp.age, emp.department)

#name is rahul and age is greate than 21

emp=session.query(Employee).filter(Employee.name=='rahul',Employee.age>21).all()
#emp=session.query(Employee).filter(Employee.age>333).one_or_none() #jaise file handling error handle karta hain waise hee ye bhi error se bachata hain