from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from flask import session
from flask import Flask, render_template, session

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5000"}})
CORS(app, resources={r"/addReview": {"origins": "http://localhost:5000"}})
CORS(app, resources={r"/authenticate": {"origins": "http://localhost:5000"},
                    r"/registerStudent": {"origins": "http://localhost:5000"}})
CORS(app, resources={r"/api/check-login-status": {"origins": "http://localhost:5000"}})


# Replace 'your_username', 'your_password', 'your_host', 'your_database' with your actual database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Gromer4211',
    'database': 'professorReviews',
}

# Function to establish a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)



from flask import request




from flask import request

# ...
@app.route('/homepage')
def homepage():
    username = session.get('username')  # Assuming you store the username in the session
    return render_template('homepage.html', username=username)


@app.route('/api/searchReviews')
def search_reviews():
    query = request.args.get('query')
    filter_option = request.args.get('filter')

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Modify the SQL query based on your database schema and filter option
        if filter_option == 'course':
            cursor.execute("SELECT * FROM feedback WHERE className LIKE %s", ('%' + query + '%',))
        elif filter_option == 'professor':
            cursor.execute("SELECT * FROM feedback WHERE profName LIKE %s", ('%' + query + '%',))
        else:
            cursor.execute("SELECT * FROM feedback WHERE profName LIKE %s OR className LIKE %s", ('%' + query + '%', '%' + query + '%'))

        reviews = cursor.fetchall()

        return jsonify({'reviews': reviews}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': f'Database error: {err}'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()


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

@app.route('/api/check-login-status', methods=['GET', 'OPTIONS'])
def check_login_status():
    print(request.headers)
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = app.make_default_options_response()
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        return response

    # For actual GET request, check the Authorization header
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return jsonify({'isLoggedIn': True}), 200
    else:
        return jsonify({'isLoggedIn': False}), 200

    

    # Add this route to handle logout
@app.route('/api/logout', methods=['POST'])
def logout():
    # Here you can perform any additional cleanup, if needed
    return jsonify({'message': 'Logged out successfully'}), 200


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

@app.route('/addReview', methods=['POST'])
def add_review():
    try:
        data = request.json
        profName = data.get('profName')
        className = data.get('className')
        rating = data.get('rating')
        reviewDescription = data.get('reviewDescription')

        print(f"Received data: profName={profName}, className={className}, rating={rating}, reviewDescription={reviewDescription}")

        connection = get_db_connection()
        cursor = connection.cursor()

        # Insert a new row into the feedback table
        cursor.execute("INSERT INTO feedback (profName, className, rating, reviewDescription) VALUES (%s, %s, %s, %s)",
                       (profName, className, rating, reviewDescription))
        connection.commit()

        print("Review added successfully")

        return jsonify({'message': 'Review added successfully'}), 201

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': 'Internal Server Error'}), 500

    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

            

@app.route('/api/getReviews', methods=['GET'])
def get_reviews():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM feedback")
        reviews = cursor.fetchall()
        return jsonify({'reviews': reviews}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
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
        cursor.execute("SELECT * FROM professor WHERE profEmail = %s", (profEmail,))

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