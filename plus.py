from flask import Flask, render_template, request
import sqlite3
import hashlib

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('plus.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT password FROM Users WHERE username=?', (username,))
        conn.commit()

        fetchall_res = cursor.fetchall()
        conn.close()

        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        if len(fetchall_res) == 0:
            # User doesn't exist
            return render_template("index.html", error='Error: No account with that username exists', version='Plus'), 400
        elif hashed_password != fetchall_res[0][0]:
            # Password does not match
            return render_template("index.html", error='Error: Incorrect password', version='Plus'), 400

        return render_template("success.html", action='logged in', username=username, version='Plus')
    
    elif request.method == 'GET':
        return render_template("index.html", version='Plus')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('plus.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT username FROM Users WHERE username=?', (username,))
        conn.commit()

        if len(cursor.fetchall()) != 0:
            # User already exists
            conn.close()
            return render_template("signup.html", error='Error: Account with that username already exists', version='Plus'), 400
        
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password,))
        conn.commit()

        return render_template("success.html", action='signed up', username=username, version='Plus')
    
    elif request.method == 'GET':
        return render_template("signup.html", version='Plus')


if __name__ == "__main__":
    conn = sqlite3.connect('plus.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Users (username TEXT, password TEXT)')
    conn.commit()

    conn.close()

    app.run(port=50102, debug=True)