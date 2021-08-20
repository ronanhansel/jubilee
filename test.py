import psycopg2
import os

DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
c = conn.cursor()
conn.autocommit = True
# c.execute("""CREATE TABLE IF NOT EXISTS employees (empno INT, ename TEXT, job TEXT, mgr INT, sal INT, comm INT, deptno INT);

# INSERT INTO employees VALUES (7788, 'SCOTT',  'ANALYST',NULL, 3000, NULL, 20);

# INSERT INTO employees VALUES (7369, 'SMITH',  'CLERK', 7788, 800, NULL, 20);

# INSERT INTO employees VALUES (7499, 'ALLEN',  'SALESMAN', 7788, 1600,  300, 10);



# CREATE TABLE IF NOT EXISTS department (DEPTNO INT, DNAME TEXT, LOC TEXT );

# INSERT INTO department VALUES (10, 'ACCOUNTING', 'NEW YORK');

# INSERT INTO department VALUES (20, 'RESEARCH',   'DALLAS');""")

# c.execute("""CREATE TABLE IF NOT EXISTS notes (key TEXT, note TEXT );

# c.execute("""INSERT INTO notes VALUES ('aa', 'sss');""")


c.execute("""
    select ename,job from employees
    where ename LIKE 'SMITH';
""")
data = c.fetchall()
print(data)