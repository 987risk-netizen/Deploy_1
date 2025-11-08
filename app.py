from flask import Flask, render_template, request, flash, redirect, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def init_db():
    """Create the SQLite database and table if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        mobile TEXT NOT NULL,
        event TEXT NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return redirect('/registration')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO registrations (name, email, mobile, event, password) VALUES (?,?,?,?,?)",
            (request.form['name'], request.form['email'], request.form['mobile'], request.form['event'], request.form['password'])
        )
        db.commit()
        last_id = cursor.lastrowid
        # fetch the newly inserted row to display
        cursor.execute('SELECT * FROM registrations WHERE id=?', (last_id,))
        reg = cursor.fetchone()
        # close DB
        cursor.close()
        db.close()
        # render page showing the registered info
        return render_template('registration.html', registered=reg)
    return render_template('registration.html')

if __name__ == '__main__':
    # ensure DB exists
    init_db()
    app.run(debug=True)
