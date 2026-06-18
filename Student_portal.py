import mysql.connector
import os
import base64
def connect_db():
    try:
        conn=mysql.connector.connect(
            host="host",
            user="root",
            password="yourpassword",
            database="student_db"
        )
        return conn
    except mysql.connector.Error as e:
        print("Database connection failed",e)
def register_student():
    conn=connect_db()
    if not conn:
        return
    cursor=conn.cursor()
    try:
        name=input("Enter Name:")
        email=input("Enter Email:")
        course=input("Enter Course:")
        with open("profile.jpeg", "rb") as file:
            binarydata=base64.b64encode(file.read())
        query="""
        Insert into students(name, email, course, profile_pic) values (%s, %s, %s, %s)
        """
        cursor.execute(query, (name,email,course,binarydata))
        conn.commit()
        print("Student registered successfully!!")
    except mysql.connector.IntegrityError:
        print("Duplicate email not allowed")
    except Exception as e:
        print("Error:",e)
    finally:
        cursor.close()
        conn.close()
def view_students():
    conn=connect_db()
    if not conn:
        return
    cursor=conn.cursor()
    cursor.execute("Select id,name,email,course from students")
    data=cursor.fetchall()
    print("\n-------Student Records--------")
    for row in data:
        print(f"ID: {row[0]} | Name: {row[1]} | Email: {row[2]} | Course: {row[3]}")
    cursor.close()
    conn.close()
def search_student():
    conn=connect_db()
    if not conn:
        return
    cursor=conn.cursor()
    student_id=input("Enter student id:")
    cursor.execute("SELECT name, email, course FROM students WHERE id=%s", (student_id,))
    result = cursor.fetchone()
    if result:
        print("\n--- STUDENT DETAILS ---")
        print("Name:", result[0])
        print("Email:", result[1])
        print("Course:", result[2])
    else:
        print("Student not found")
    cursor.close()
    conn.close()
def restore_img():
    conn=connect_db()
    if not conn:
        return
    cursor=conn.cursor()
    student_id=input("Enter student id:")
    cursor.execute("SELECT profile_pic FROM students WHERE id=%s", (student_id,))
    result = cursor.fetchone()
    if result and result[0]:
        image_data = base64.b64decode(result[0])
        output_file = f"restored_student_{student_id}.jpg"
        with open(output_file, "wb") as file:
            file.write(image_data)
        print(f"Image restored as {output_file}")
    else:
        print("Image not found!")
    cursor.close()
    conn.close()
def update_student():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    student_id = input("Enter Student ID to update: ")
    name = input("New Name: ")
    email = input("New Email: ")
    course = input("New Course: ")
    query = """
    UPDATE students
    SET name=%s, email=%s, course=%s
    WHERE id=%s
    """
    cursor.execute(query, (name, email, course, student_id))
    conn.commit()
    if cursor.rowcount > 0:
        print("Student Updated Successfully!")
    else:
        print("Student not found!")
    cursor.close()
    conn.close()
def delete_student():
    conn = connect_db()
    if not conn:
        return
    cursor = conn.cursor()
    student_id = input("Enter Student ID to delete: ")
    cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
    conn.commit()
    if cursor.rowcount > 0:
        print("Student Deleted Successfully!")
    else:
        print("Student not found!")
    cursor.close()
    conn.close()
def menu():
    while True:
        print("\n------------STUDENT REGISTRATION PORTAL ------------")
        print("1. Register Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Restore Profile Picture")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            register_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student()
        elif choice == "4":
            restore_img()
        elif choice == "5":
            update_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            print("Exiting... ")
            break
        else:
            print("Invalid choice!")
menu()