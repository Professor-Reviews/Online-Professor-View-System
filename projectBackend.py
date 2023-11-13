from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your actual database connection details
db_config = {
    'host': 'host',
    'user': 'username',
    'password': 'your_password',
    'database': 'your_database',
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json  # Assuming the data is sent as JSON in the request body

    studentEmail = data.get('studentEmail')
    password = data.get('password')

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT studentEmail, password FROM Student WHERE studentEmail = %s AND Password = %s", (studentEmail, password))
        student = cursor.fetchone()

        if student:
            return jsonify({'authenticated': True}), 200
        else:
            return jsonify({'authenticated': False}), 401

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

# Flask route for student registration
@app.route('/registerStudent', methods=['POST'])
def add_student():
    data = request.json  # Assuming the data is sent as JSON in the request body

    fName = data.get('fName')
    lName = data.get('lName')
    studentEmail = data.get('studentEmail')
    password = data.get('password')
    #print(fName + lName + studentEmail + password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if a row with the given email already exists
        cursor.execute("SELECT * FROM Student WHERE studentEmail = %s", (studentEmail,))
        existing_student = cursor.fetchone()

        if existing_student:
            return jsonify({'message': 'User with the email already exists'}), 409  # 409 Conflict status code

        # Insert a new row if the email doesn't exist
        cursor.execute("INSERT INTO Student (fName, lName, studentEmail, password) VALUES (%s, %s, %s, %s)",
                       (fName, lName, studentEmail, password))
        connection.commit()

        return jsonify({'message': 'User added successfully'}), 201  # 201 Created status code

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

@app.route('/getStudentData', methods=['GET'])
def get_student_data():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Fetch all student data from the database
        cursor.execute("SELECT * FROM Student")
        students = cursor.fetchall()

        return jsonify({'students': students}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

@app.route('/addFeedback', methods=['POST'])
def add_feedback():
    data = request.json

    profName = data.get('profName')
    university = data.get('university')
    rating = data.get('rating')
    feedback_input = data.get('input')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert a new row into the feedback table
        cursor.execute("INSERT INTO feedback (profName, university, rating, input) VALUES (%s, %s, %s, %s)",
                       (profName, university, rating, feedback_input))
        connection.commit()

        return jsonify({'message': 'Feedback added successfully'}), 201  # 201 Created status code

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

@app.route('/registerProfessor', methods=['POST'])
def add_professor():
    data = request.json  # Assuming the data is sent as JSON in the request body

    fName = data.get('fName')
    lName = data.get('lName')
    profEmail = data.get('profEmail')
    password = data.get('password')
    #print(fName + lName + studentEmail + password)
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if a row with the given email already exists
        cursor.execute("SELECT * FROM professor WHERE studentEmail = %s", (profEmail,))
        existing_student = cursor.fetchone()

        if existing_student:
            return jsonify({'message': 'User with the email already exists'}), 409  # 409 Conflict status code

        # Insert a new row if the email doesn't exist
        cursor.execute("INSERT INTO professor (fName, lName, profEmail, password) VALUES (%s, %s, %s, %s)",
                       (fName, lName, profEmail, password))
        connection.commit()

        return jsonify({'message': 'User added successfully'}), 201  # 201 Created status code

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
