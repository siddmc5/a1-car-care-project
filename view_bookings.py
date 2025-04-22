import sqlite3

# Connect to the database
conn = sqlite3.connect('bookings.db')
cursor = conn.cursor()

# Fetch all bookings
cursor.execute('SELECT * FROM bookings')
bookings = cursor.fetchall()

# Display the results
print("\nAll Bookings:")
for booking in bookings:
    print(f"ID: {booking[0]}, Name: {booking[1]}, Phone: {booking[2]}, Vehicle: {booking[3]}, Service: {booking[4]}, Date: {booking[5]}")

conn.close()
