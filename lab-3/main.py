import sqlite3
import time

connection = None
cursor = None


def connect(path):
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA foreign_keys=ON; ')
    connection.commit()
    return


def drop_tables():
    global connection, cursor

    drop_course = "DROP TABLE IF EXISTS course; "
    drop_student = "DROP TABLE IF EXISTS student; "
    drop_enroll = "DROP TABLE IF EXISTS enroll; "

    cursor.execute(drop_enroll)
    cursor.execute(drop_student)
    cursor.execute(drop_course)


def define_tables():
    global connection, cursor

    course_query = '''
                        CREATE TABLE course (
                                    course_id INTEGER,
                                    title TEXT,
                                    seats_available INTEGER,
                                    PRIMARY KEY (course_id)
                                    );
                    '''

    student_query = '''
                        CREATE TABLE student (
                                    student_id INTEGER,
                                    name TEXT,
                                    PRIMARY KEY (student_id)
                                    );
                    '''

    enroll_query = '''
                    CREATE TABLE enroll (
                                student_id INTEGER,
                                course_id INTEGER,
                                enroll_date DATE,
                                PRIMARY KEY (student_id, course_id),
                                FOREIGN KEY(student_id) REFERENCES student(student_id),
                                FOREIGN KEY(course_id) REFERENCES course(course_id)
                                );
                '''

    cursor.execute(course_query)
    cursor.execute(student_query)
    cursor.execute(enroll_query)
    connection.commit()

    return


def insert_data():
    global connection, cursor

    insert_courses = '''
                        INSERT INTO course(course_id, title, seats_available) VALUES
                            (1, 'CMPUT 291', 200),
                            (2, 'CMPUT 391', 100),
                            (3, 'CMPUT 101', 300);
                    '''

    insert_students = '''
                            INSERT INTO student(student_id, name) VALUES
                                    (1509106, 'Jeff'),
                                    (1409106, 'Alex'),
                                    (1609106, 'Mike');
                            '''

    cursor.execute(insert_courses)
    cursor.execute(insert_students)
    connection.commit()
    return


def enroll(student_id, course_id):
    global connection, cursor

    current_date = time.strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("SELECT seats_available FROM course c WHERE c.course_id = :id ",{"id":course_id})
    seats = cursor.fetchone()[0]

    if seats > 0:
        cursor.execute("INSERT INTO enroll(student_id, course_id, enroll_date) VALUES (:sid, :cid, :date)", {"sid" : student_id, "cid":course_id, "date":current_date})
        cursor.execute("UPDATE course SET seats_available = :new_seats WHERE course_id = :cid", {"new_seats":seats-1, "cid":course_id}) 
    

    # Printing seats:
    cursor.execute("SELECT seats_available FROM course c WHERE c.course_id = :id ",{"id":course_id})
    seats = cursor.fetchone()[0]
    # connection.commit()
    print(seats)
    
    return


def main():
    global connection, cursor

    path = "./register.db"
    connect(path)
    drop_tables()
    define_tables()
    insert_data()

    # register all students in all courses:

    cursor.execute("SELECT course_id FROM course")
    courses = cursor.fetchall()
    cursor.execute("SELECT student_id FROM student")
    students = cursor.fetchall()

    for i in students:
        print("-------------")
        for j in courses:
            enroll(i[0],j[0])


    # connection.commit()
    connection.close()
    connect(path)

    cursor.execute("SELECT * FROM course")
    students = cursor.fetchall()
    print(students)

    # cursor.execute("SELECT * FROM course")
    # students = cursor.fetchall()
    # print(students

    return


if __name__ == "__main__":
    main()