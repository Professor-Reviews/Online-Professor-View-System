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

    username = data.get('username')
    password = data.get('password')

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT Username, Password FROM Student WHERE Username = %s AND Password = %s", (username, password))
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
@app.route('/register', methods=['POST'])
def student_registration():
    data = request.json  # Assuming the data is sent as JSON in the request body

    email = data.get('email')
    username = data.get('username')
    fname = data.get('fname')
    lname = data.get('lname')
    password = data.get('password')

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT email FROM Student WHERE email = %s", (email,))
        existing_student = cursor.fetchone()

        if existing_student:
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        else:
            cursor.execute("INSERT INTO Student (email, username, fname, lname, password) VALUES (%s, %s, %s, %s, %s)",
                           (email, username, fname, lname, password))
            connection.commit()

            return jsonify({'success': True, 'message': 'Student registered successfully'}), 201

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
