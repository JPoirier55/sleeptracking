from flask import Flask, render_template, request, redirect, url_for, send_file
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)


# add get off

def run_postgres_query(sql, data):
    connection = psycopg2.connect(
        host="192.168.1.20",
        database="fitbit",
        user="fitbit",
        password="password",
        port=5435
    )
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute(sql, data) 
    records = None
    if 'SELECT' in sql:
        records = cursor.fetchall()
    connection.commit()

    cursor.close()
    return records

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date = request.form['date']
        nap = request.form.get('nap', 'No')
        alcohol = request.form.get('alcohol', 'No') 
        food = request.form.get('food', 'none')
        activity = request.form['activity']
        stretching = request.form.get('stretching', 'No') 
        caffeine = request.form['caffeine']
        sleep_quality = request.form['sleep_quality']

        data = (date, nap, alcohol, food, activity, stretching, caffeine, sleep_quality)

        sql = f"""
        INSERT INTO manual_sleep_data (date, nap, alcohol, food, activity, stretching, caffeine, sleep_quality)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        run_postgres_query(sql, data) 

        return redirect(url_for('data'))

    return render_template('index.html')

@app.route('/data', methods=['GET'])
def data():
    sql = """SELECT id, date, nap, alcohol, food, activity, stretching, caffeine, sleep_quality FROM manual_sleep_data"""
    records = run_postgres_query(sql, None)
    return render_template('data.html', records=records)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        # Update the record with the new data
        date = request.form['date']
        nap = request.form.get('nap', 'No')
        alcohol = request.form.get('alcohol', 'No')
        food = request.form['food']
        activity = request.form['activity']
        stretching = request.form.get('stretching', 'No')
        caffeine = request.form['caffeine']
        sleep_quality = request.form['sleep_quality']

        sql = """UPDATE manual_sleep_data SET date = %s, nap = %s, alcohol = %s, food = %s, activity = %s, stretching = %s, caffeine = %s, sleep_quality = %s WHERE id = %s"""

        run_postgres_query(sql, (date, alcohol, nap, food, activity, stretching, caffeine, sleep_quality, id))

        return redirect(url_for('data'))
    else:
        sql = """SELECT * FROM manual_sleep_data WHERE id = %s"""
        record = run_postgres_query(sql, (id,))
        print(record)
        return render_template('edit.html', record=record[0])

@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    sql = """DELETE FROM manual_sleep_data WHERE id = %s"""
    run_postgres_query(sql, (id,))
    return redirect(url_for('data'))

# @app.route('/graph', methods=['GET'])
# def graph():
#     # Retrieve data from the database
#     conn = sqlite3.connect('manual_sleep_data.db')
#     c = conn.cursor()
#     c.execute('''SELECT date, sleep_hours FROM manual_sleep_data''')
#     records = c.fetchall()
#     conn.close()

#     # Prepare data for rendering
#     dates = [record[0] for record in records]
#     sleep_hours = [record[1] for record in records]

#     # Render the graph page
#     return render_template('graph.html', dates=dates, sleep_hours=sleep_hours)

# @app.route('/export', methods=['GET'])
# def export():
#     # Export data to CSV
#     conn = sqlite3.connect('manual_sleep_data.db')
#     c = conn.cursor()
#     c.execute('''SELECT date, sleep_hours, temperature, alcohol, food, activity, stretching, caffeine, sleep_quality, bedtime, awaketime FROM manual_sleep_data''')
#     records = c.fetchall()
#     conn.close()

#     # Define CSV file path
#     csv_file_path = 'manual_sleep_data.csv'
#     with open(csv_file_path, 'w', newline='') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerow(['Date', 'Sleep Hours', 'Temperature', 'Alcohol', 'Food', 'Activity', 'Stretching', 'Caffeine', 'Sleep Quality', 'Bedtime', 'Awaketime'])
#         csvwriter.writerows(records)

#     return send_file(csv_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
