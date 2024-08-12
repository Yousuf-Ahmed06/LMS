import sqlite3 as sql
import time

conn = sql.connect('rosterdb.sqlite')
cur = conn.cursor()
selection = 1
while selection != 0:
    selection:int = int(input("""
        Welcome to the Learning Management System \n
        Press 1: Add new admission \n
        Press 2: Fetch a member\'s data \n
        Press 3: Fetch data about a course \n
        Press 0: Exit
    """))
    if selection == 1:
        name = input("Please enter member\'s name: ")
        course =  input("Please input course name or course ID: ")
        status = int(input("Please input 0 if the member is a student and 1 if the member is a teacher: "))

        try:
            cur.execute('INSERT INTO User (name) VALUES ( ? )', (name, ))
            cur.execute('SELECT id FROM User WHERE name = ?', (name, ))
            student_id:int = cur.fetchone()[0]
            cur.execute('SELECT id FROM Course WHERE title = ?', (course, ))
            course_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Member (user_id, course_id, role) VALUES ( ?, ?, ? )", (student_id, course_id, status, ))
            if status == 0: role = "student"
            elif status == 1: role = "teacher"
            print(f"New User {name} added into {course}, with role \"{role}\"")
        except:
            print(f"User {name} already exists!!!")
            continue
    elif selection == 2:
        name:str = input("Please enter member\'s name: ")
        try:
            cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
            user_id = cur.fetchone()[0]
            cur.execute('SELECT course_id FROM Member WHERE user_id = ?', (user_id, ))
            course_id:int = cur.fetchone()[0]
            cur.execute('SELECT title FROM Course WHERE id = ?', (course_id, ))
            course:str = cur.fetchone()[0]
            print(f'Student Name: {name}, Course selected: {course}')
        except:
            print('User doesn\'t exist, please recheck spelling or create a new record!!.')
            continue
    elif selection == 3:
        course = input("PLease input course name: ")
        cur.execute('SELECT id FROM Course WHERE title = ?', (course, ))
        course_id = cur.fetchone()[0]
        cur.execute('SELECT user_id FROM Member WHERE course_id = ?', (course_id, ))
        student_id = cur.fetchall()
        mem_lst = [str(s).strip("(,')") for s in student_id]
        seql = "SELECT name FROM User WHERE id IN (%s)" % ",".join("?"*len(mem_lst))
        cur.execute(seql, mem_lst)
        names = cur.fetchall()
        names = [str(v).strip("(,)") for v in names]
        print("Course Members: \n")
        print([p for p in names])