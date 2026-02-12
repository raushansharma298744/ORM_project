import psycopg2
conn=psycopg2.connect(
    host="localhost",
    database="school",
    user="postgres",
    password="12345"
)
print("connection done")
cur=conn.cursor()
cur.execute("DROP TABLE IF EXISTS employees")
cur.execute("CREATE TABLE employees ( id INT, name VARCHAR(50), salary INT) ")
cur.execute("INSERT INTO employees VALUES (1,'rahul',50000) ")
conn.commit()
cur.execute("SELECT * from employees")
rows=cur.fetchall()
for i in rows:
    print(i)
cur.close()
conn.close()
