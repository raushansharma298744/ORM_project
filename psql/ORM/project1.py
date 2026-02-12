# =====================================
# LIBTRACK - CLI LIBRARY SYSTEM
# =====================================

# ---------- IMPORTS ----------

# Used to create database connection and write SQL queries
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, text

# Used to define ORM tables and database session
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


# ---------- DATABASE CONNECTION ----------

# Creates SQLite database file named libtrack.db
# echo=True prints SQL queries for learning purpose
engine = create_engine("sqlite:///libtrack.db", echo=True)

# Base class for ORM models
Base = declarative_base()

# Session class (acts like cursor)
Session = sessionmaker(bind=engine)

# Create session object
session = Session()


# ---------- TABLE DEFINITIONS ----------

# Category table
class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)   # unique category id
    name = Column(String)                    # category name

    # One category → many books
    books = relationship("Book", back_populates="category")


# Book table
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)   # book id
    title = Column(String)                   # book title
    author = Column(String)                  # book author

    category_id = Column(Integer, ForeignKey("categories.id"))

    # Link book to category
    category = relationship("Category", back_populates="books")

    # One book → many borrows
    borrows = relationship("Borrow", back_populates="book")


# Borrow table
class Borrow(Base):
    __tablename__ = "borrows"

    id = Column(Integer, primary_key=True)   # borrow id
    borrow_date = Column(String)             # date borrowed

    book_id = Column(Integer, ForeignKey("books.id"))

    # Link borrow to book
    book = relationship("Book", back_populates="borrows")


# Monthly limit table
class Limit(Base):
    __tablename__ = "limits"

    id = Column(Integer, primary_key=True)
    month = Column(String)                   # YYYY-MM
    max_books = Column(Integer)              # allowed borrows


# Create tables in database
Base.metadata.create_all(engine)


# ---------- FUNCTIONS ----------

def add_category():
    # Ask user for category name
    name = input("Category name: ")

    # Create Category object and save
    session.add(Category(name=name))
    session.commit()

    print("✅ Category added")


def add_book():
    title = input("Book title: ")
    author = input("Author name: ")
    category_id = int(input("Category ID: "))

    # Create Book object
    session.add(Book(title=title, author=author, category_id=category_id))
    session.commit()

    print("✅ Book added")


def borrow_book():
    book_id = int(input("Book ID: "))
    date = input("Borrow date (YYYY-MM-DD): ")

    # Create Borrow record
    session.add(Borrow(book_id=book_id, borrow_date=date))
    session.commit()

    print("✅ Book borrowed")


def update_borrow():
    bid = int(input("Borrow ID: "))

    # Find borrow record
    borrow = session.query(Borrow).filter(Borrow.id == bid).first()

    if borrow:
        borrow.borrow_date = input("New date: ")
        session.commit()
        print("✅ Borrow updated")
    else:
        print("❌ Borrow not found")


def delete_borrow():
    bid = int(input("Borrow ID: "))

    borrow = session.query(Borrow).filter(Borrow.id == bid).first()

    if borrow:
        session.delete(borrow)
        session.commit()
        print("✅ Borrow deleted")
    else:
        print("❌ Borrow not found")


def search_by_date():
    date = input("Enter date: ")

    borrows = session.query(Borrow).filter(Borrow.borrow_date == date).all()

    for b in borrows:
        print(b.book.title, "-", b.borrow_date)


# ---------- RAW SQL REPORT ----------

def category_report():
    sql = """
    SELECT categories.name, COUNT(borrows.id)
    FROM categories
    JOIN books ON categories.id = books.category_id
    JOIN borrows ON books.id = borrows.book_id
    GROUP BY categories.name
    """

    result = session.execute(text(sql))

    print("\n📊 Category Wise Borrow Report")
    for row in result:
        print(row[0], "→", row[1])


def set_limit():
    month = input("Month (YYYY-MM): ")
    max_books = int(input("Max books allowed: "))

    session.add(Limit(month=month, max_books=max_books))
    session.commit()

    print("✅ Monthly limit set")


def limit_alert():
    month = input("Month (YYYY-MM): ")

    # Count borrows for month
    total = session.execute(
        text("SELECT COUNT(*) FROM borrows WHERE borrow_date LIKE :m"),
        {"m": f"{month}%"}
    ).scalar()

    limit = session.query(Limit).filter(Limit.month == month).first()

    if limit and total > limit.max_books:
        print("⚠️ Borrow limit exceeded")
    else:
        print("✅ Within borrow limit")


# ---------- CLI MENU ----------

while True:
    print("""
===== LIBTRACK =====
1. Add Category
2. Add Book
3. Borrow Book
4. Update Borrow
5. Delete Borrow
6. Search Borrow by Date
7. Category Borrow Report
8. Set Monthly Limit
9. Limit Alert
10. Exit
""")

    choice = input("Choose: ")

    if choice == "1":
        add_category()
    elif choice == "2":
        add_book()
    elif choice == "3":
        borrow_book()
    elif choice == "4":
        update_borrow()
    elif choice == "5":
        delete_borrow()
    elif choice == "6":
        search_by_date()
    elif choice == "7":
        category_report()
    elif choice == "8":
        set_limit()
    elif choice == "9":
        limit_alert()
    elif choice == "10":
        break
    else:
        print("❌ Invalid choice")