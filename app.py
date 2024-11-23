import csv
from flask import Flask, render_template, request, redirect, url_for, send_file
import sqlite3

app = Flask(__name__)


# nap
# workout
# 


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the form
        date = request.form['date']
        sleep_hours = request.form['sleep_hours']
        temperature = request.form['temperature']
        alcohol = request.form.get('alcohol', 'No')  # Defaults to 'No' if not checked
        food = request.form['food']
        activity = request.form['activity']
        stretching = request.form.get('stretching', 'No')  # Defaults to 'No' if not checked
        caffeine = request.form['caffeine']
        sleep_quality = request.form['sleep_quality']
        bedtime = request.form['bedtime']
        awaketime = request.form['awaketime']

        # Save data to the database
        conn = sqlite3.connect('health_data.db')
        c = conn.cursor()
        c.execute('''INSERT INTO health_data (date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime))
        conn.commit()
        conn.close()

        return redirect(url_for('data'))

    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    # Retrieve data from the database
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''SELECT id, date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime FROM health_data''')
    records = c.fetchall()
    conn.close()

    # Render the data page
    return render_template('data.html', records=records)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    if request.method == 'POST':
        # Update the record with the new data
        date = request.form['date']
        sleep_hours = request.form['sleep_hours']
        temperature = request.form['temperature']
        alcohol = request.form.get('alcohol', 'No')
        food = request.form['food']
        activity = request.form['activity']
        stretching = request.form.get('stretching', 'No')
        caffeine = request.form['caffeine']
        sleep_quality = request.form['sleep_quality']
        bedtime = request.form['bedtime']
        awaketime = request.form['awaketime']

        c.execute('''UPDATE health_data SET date = ?, sleep_hours = ?, temperature = ?, alcohol = ?, food = ?, activity = ?, stretching = ?, caffeine = ?, sleep_quality = ?, bedtime = ?, awaketime = ? WHERE id = ?''',
                  (date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime, id))
        conn.commit()
        conn.close()
        return redirect(url_for('data'))
    else:
        # Retrieve the current data for the record to be edited
        c.execute('''SELECT * FROM health_data WHERE id = ?''', (id,))
        record = c.fetchone()
        conn.close()
        return render_template('edit.html', record=record)

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # Delete the record from the database
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''DELETE FROM health_data WHERE id = ?''', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('data'))

@app.route('/graph', methods=['GET'])
def graph():
    # Retrieve data from the database
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''SELECT date, sleep_hours FROM health_data''')
    records = c.fetchall()
    conn.close()

    # Prepare data for rendering
    dates = [record[0] for record in records]
    sleep_hours = [record[1] for record in records]

    # Render the graph page
    return render_template('graph.html', dates=dates, sleep_hours=sleep_hours)

@app.route('/export', methods=['GET'])
def export():
    # Export data to CSV
    conn = sqlite3.connect('health_data.db')
    c = conn.cursor()
    c.execute('''SELECT date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime FROM health_data''')
    records = c.fetchall()
    conn.close()

    # Define CSV file path
    csv_file_path = 'health_data.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Date', 'Sleep Hours', 'Temperature', 'Alcohol', 'Food', 'Activity', 'Stretching', 'Caffeine', 'Sleep Quality', 'Bedtime', 'Awaketime'])
        csvwriter.writerows(records)

    return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
