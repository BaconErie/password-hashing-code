from flask import Flask, render_template, request
import sqlite3
import bcrypt

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('enterprise.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT password FROM Users WHERE username=?', (username,))
        conn.commit()

        fetchall_res = cursor.fetchall()
        conn.close()

        if len(fetchall_res) == 0:
            # User doesn't exist
            return render_template("index.html", error='Error: No account with that username exists', version='Enterprise'), 400
        elif not bcrypt.checkpw(password.encode('utf-8'), fetchall_res[0][0].encode('utf-8')):
            # Password does not match
            return render_template("index.html", error='Error: Incorrect password', version='Enterprise'), 400

        return render_template("success.html", action='logged in', username=username, version='Enterprise')
    
    elif request.method == 'GET':
        return render_template("index.html", version='Enterprise')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('enterprise.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT username FROM Users WHERE username=?', (username,))
        conn.commit()

        if len(cursor.fetchall()) != 0:
            # User already exists
            conn.close()
            return render_template("signup.html", error='Error: Account with that username already exists', version='Enterprise'), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_password = hashed_password.decode('utf-8')

        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, hashed_password,))
        conn.commit()

        return render_template("success.html", action='signed up', username=username, password=password, version='Enterprise')
    
    elif request.method == 'GET':
        return render_template("signup.html", version='Enterprise')


if __name__ == "__main__":
    conn = sqlite3.connect('enterprise.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Users (username TEXT, password TEXT)')
    conn.commit()

    conn.close()

    app.run(port=50103, debug=True)