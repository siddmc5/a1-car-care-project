import os
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3
app = Flask(__name__)
CORS(app)
# Initialize database
def init_db():
    # Using a relative path so it works correctly on Render
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        vehicle TEXT,
        service TEXT,
        date TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/book', methods=['POST'])
def book():
    data = request.form
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('INSERT INTO bookings (name, phone, vehicle, service, date) VALUES (?, ?, ?, ?, ?)',
              (data['name'], data['phone'], data['vehicle'], data['service'], data['date']))
    conn.commit()
    conn.close()
    return redirect('/thankyou')


@app.route('/admin')
def admin():
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

@app.route('/thankyou')
def thankyou():
    return "Thank you for your booking!"

if __name__ == '__main__':
    # Use the port specified by Render
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port, debug=True)
