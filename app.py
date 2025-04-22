import os
from flask import Flask, request, render_template, redirect
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

# Initialize new database and create the bookings table
def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')
    
    # Check if the database file already exists
    if not os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        
        # Create the bookings table if it doesn't exist
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
        print(f"Database created at {db_path}")
    else:
        print("Database already exists.")

# Call init_db when app starts
init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    data = request.form
    db_path = os.path.join(os.path.dirname(__file__), 'bookings.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    try:
        # Insert booking data into the database
        c.execute('INSERT INTO bookings (name, phone, vehicle, service, date) VALUES (?, ?, ?, ?, ?)',
                  (data['name'], data['phone'], data['vehicle'], data['service'], data['date']))
        conn.commit()
        print("Booking added successfully.")
    except Exception as e:
        print(f"Error adding booking: {e}")
    finally:
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
    # Run the app on the correct host and port
    port = int(os.environ.get('PORT', 5000))  # Default to 5000 if PORT not set
    app.run(host='0.0.0.0', port=port, debug=True)
