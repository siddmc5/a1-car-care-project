import os
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize database
def init_db():
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
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')  # FIXED PATH
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('INSERT INTO bookings (name, phone, vehicle, service, date) VALUES (?, ?, ?, ?, ?)',
              (data['name'], data['phone'], data['vehicle'], data['service'], data['date']))
    conn.commit()
    conn.close()

    print(f"Booking saved: {data['name']} - {data['service']}")  # Debugging log

    return redirect('/thankyou')

@app.route('/admin')
def admin():
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()
    conn.close()

    print("Bookings retrieved for admin view:", bookings)  # Debugging log

    return render_template('admin.html', bookings=bookings)

@app.route('/thankyou')
def thankyou():
    return "Thank you for your booking!"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
