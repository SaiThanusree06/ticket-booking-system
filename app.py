from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book():
    name = request.form['name']
    email = request.form['email']
    showtime = request.form['showtime']
    tickets = int(request.form['seats'])

    # Backend validation
    valid_showtimes = [
        "Morning Show - 10:00 AM",
        "Matinee Show - 1:00 PM",
        "Evening Show - 4:00 PM",
        "Night Show - 7:00 PM"
    ]

    if showtime not in valid_showtimes:
        return "❌ Invalid showtime selected!", 400

    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (name, email, showtime, tickets) VALUES (?, ?, ?, ?)",
              (name, email, showtime, tickets))
    conn.commit()
    conn.close()

    return render_template('success.html')


@app.route('/bookings')
def bookings():
    conn = sqlite3.connect('bookings.db')
    conn.row_factory = sqlite3.Row  # to access columns by name
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()
    conn.close()
    return render_template('bookings.html', bookings=rows)

@app.route('/cleanup')
def cleanup():
    conn = sqlite3.connect('bookings.db')
    c = conn.cursor()

    fixes = {
        '10 AM': 'Morning Show - 10:00 AM',
        '7': 'Night Show - 7:00 PM',
        '-4': 'Evening Show - 4:00 PM'
    }

    for wrong, correct in fixes.items():
        c.execute("UPDATE bookings SET showtime = ? WHERE showtime = ?", (correct, wrong))

    conn.commit()
    conn.close()
    return "✅ Showtimes cleaned successfully!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

