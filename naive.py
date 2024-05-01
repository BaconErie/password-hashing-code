from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('naive.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT password FROM Users WHERE username=?', (username,))
        conn.commit()

        fetchall_res = cursor.fetchall()
        conn.close()

        if len(fetchall_res) == 0:
            # User doesn't exist
            return render_template("index.html", error='Error: No account with that username exists', version='Free'), 400
        elif password != fetchall_res[0][0]:
            # Password does not match
            return render_template("index.html", error='Error: Incorrect password', version='Free'), 400

        return render_template("success.html", action='logged in', username=username, version='Free')
    
    elif request.method == 'GET':
        return render_template("index.html", version='Free')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = sqlite3.connect('naive.db')
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute('SELECT username FROM Users WHERE username=?', (username,))
        conn.commit()

        if len(cursor.fetchall()) != 0:
            # User already exists
            conn.close()
            return render_template("signup.html", error='Error: Account with that username already exists', version='Free'), 400
        

        cursor.execute('INSERT INTO Users (username, password) VALUES (?, ?)', (username, password,))
        conn.commit()

        return render_template("success.html", action='signed up', username=username, password=password, version='Free')
    
    elif request.method == 'GET':
        return render_template("signup.html", version='Free')


if __name__ == "__main__":
    conn = sqlite3.connect('naive.db')
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS Users (username TEXT, password TEXT)')
    conn.commit()

    conn.close()

    app.run(port=50101, debug=True)