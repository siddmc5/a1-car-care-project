from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bookings.db')
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
    return 'Backend running!'

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
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute('SELECT * FROM bookings')
    bookings = c.fetchall()
    conn.close()
    return render_template('admin.html', bookings=bookings)

@app.route('/thankyou')
def thankyou():
    return "Thank you for your booking!"

if __name__ == '__main__':
    app.run(debug=True)
