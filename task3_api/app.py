# ============================================================
# Task 3: REST API for Energy Consumption Data
# Connects to both MySQL and MongoDB Atlas
# Provides CRUD operations and time series query endpoints
# ============================================================

from flask import Flask, jsonify, request
from pymongo import MongoClient
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# ------------------------------------------------------------
# Database Connections
# ------------------------------------------------------------

def get_mysql():
    """Create and return a MySQL database connection."""
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )

def get_mongo():
    """Create and return a MongoDB collection connection."""
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client[os.getenv('MONGO_DB')]
    return db['energy_readings']

# ============================================================
# MySQL Endpoints
# ============================================================

# GET all readings from MySQL (limited to 100 for performance)
@app.route('/mysql/readings', methods=['GET'])
def mysql_get_readings():
    try:
        conn = get_mysql()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.reading_id, t.datetime, e.consumption, rg.region_name
            FROM energy_readings e
            JOIN time_dimension t  ON e.time_id   = t.time_id
            JOIN regions rg        ON e.region_id = rg.region_id
            ORDER BY t.datetime DESC
            LIMIT 100
        """)
        rows = cursor.fetchall()
        # Convert datetime objects to strings for JSON response
        for row in rows:
            row['datetime'] = str(row['datetime'])
        conn.close()
        return jsonify(rows), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# GET latest reading from MySQL
@app.route('/mysql/readings/latest', methods=['GET'])
def mysql_latest():
    try:
        conn = get_mysql()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.datetime, e.consumption, rg.region_name
            FROM energy_readings e
            JOIN time_dimension t  ON e.time_id   = t.time_id
            JOIN regions rg        ON e.region_id = rg.region_id
            ORDER BY t.datetime DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        row['datetime'] = str(row['datetime'])
        conn.close()
        return jsonify(row), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# GET readings by date range from MySQL
@app.route('/mysql/readings/range', methods=['GET'])
def mysql_range():
    try:
        start = request.args.get('start')
        end   = request.args.get('end')
        conn  = get_mysql()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT t.datetime, e.consumption, rg.region_name
            FROM energy_readings e
            JOIN time_dimension t  ON e.time_id   = t.time_id
            JOIN regions rg        ON e.region_id = rg.region_id
            WHERE t.datetime BETWEEN %s AND %s
            ORDER BY t.datetime ASC
        """, (start, end))
        rows = cursor.fetchall()
        for row in rows:
            row['datetime'] = str(row['datetime'])
        conn.close()
        return jsonify(rows), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# POST a new reading to MySQL
@app.route('/mysql/readings', methods=['POST'])
def mysql_create():
    try:
        data     = request.json
        dt       = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
        conn     = get_mysql()
        cursor   = conn.cursor()

        # Determine season from month
        month    = dt.month
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Autumn'

        is_weekend = dt.weekday() >= 5

        # Insert into time_dimension first
        cursor.execute("""
            INSERT IGNORE INTO time_dimension
            (datetime, hour, day, month, year, day_of_week, season, is_weekend)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (dt, dt.hour, dt.day, dt.month, dt.year, dt.weekday(), season, is_weekend))

        cursor.execute("SELECT time_id FROM time_dimension WHERE datetime = %s", (dt,))
        time_id = cursor.fetchone()[0]

        # Insert the reading
        cursor.execute("""
            INSERT INTO energy_readings (region_id, time_id, consumption)
            VALUES (1, %s, %s)
        """, (time_id, data['consumption']))

        conn.commit()
        conn.close()
        return jsonify({'message': 'Reading created successfully'}), 201
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# PUT update a reading in MySQL
@app.route('/mysql/readings/<int:reading_id>', methods=['PUT'])
def mysql_update(reading_id):
    try:
        data   = request.json
        conn   = get_mysql()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE energy_readings SET consumption = %s WHERE reading_id = %s
        """, (data['consumption'], reading_id))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Reading {reading_id} updated successfully'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# DELETE a reading from MySQL
@app.route('/mysql/readings/<int:reading_id>', methods=['DELETE'])
def mysql_delete(reading_id):
    try:
        conn   = get_mysql()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM energy_readings WHERE reading_id = %s", (reading_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': f'Reading {reading_id} deleted successfully'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ============================================================
# MongoDB Endpoints
# ============================================================

# GET all readings from MongoDB (limited to 100)
@app.route('/mongo/readings', methods=['GET'])
def mongo_get_readings():
    try:
        collection = get_mongo()
        readings   = list(collection.find({}, {'_id': 0}).limit(100))
        return jsonify(readings), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# GET latest reading from MongoDB
@app.route('/mongo/readings/latest', methods=['GET'])
def mongo_latest():
    try:
        collection = get_mongo()
        reading    = collection.find_one({}, {'_id': 0}, sort=[('datetime', -1)])
        return jsonify(reading), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# GET readings by date range from MongoDB
@app.route('/mongo/readings/range', methods=['GET'])
def mongo_range():
    try:
        start      = request.args.get('start')
        end        = request.args.get('end')
        collection = get_mongo()
        readings   = list(collection.find({
            'datetime': {'$gte': start, '$lte': end}
        }, {'_id': 0}).sort('datetime', 1))
        return jsonify(readings), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# POST a new reading to MongoDB
@app.route('/mongo/readings', methods=['POST'])
def mongo_create():
    try:
        data       = request.json
        dt         = datetime.strptime(data['datetime'], '%Y-%m-%d %H:%M:%S')
        month      = dt.month
        if month in [12, 1, 2]:
            season = 'Winter'
        elif month in [3, 4, 5]:
            season = 'Spring'
        elif month in [6, 7, 8]:
            season = 'Summer'
        else:
            season = 'Autumn'

        document = {
            'datetime'       : data['datetime'],
            'consumption_mw' : data['consumption'],
            'region'         : 'AEP',
            'time_components': {
                'hour'       : dt.hour,
                'day'        : dt.day,
                'month'      : dt.month,
                'year'       : dt.year,
                'day_of_week': dt.weekday(),
                'season'     : season,
                'is_weekend' : dt.weekday() >= 5
            }
        }
        collection = get_mongo()
        collection.insert_one(document)
        return jsonify({'message': 'Reading created successfully'}), 201
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# PUT update a reading in MongoDB
@app.route('/mongo/readings/<datetime_str>', methods=['PUT'])
def mongo_update(datetime_str):
    try:
        data       = request.json
        collection = get_mongo()
        collection.update_one(
            {'datetime': datetime_str},
            {'$set': {'consumption_mw': data['consumption']}}
        )
        return jsonify({'message': f'Reading for {datetime_str} updated successfully'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# DELETE a reading from MongoDB
@app.route('/mongo/readings/<datetime_str>', methods=['DELETE'])
def mongo_delete(datetime_str):
    try:
        collection = get_mongo()
        collection.delete_one({'datetime': datetime_str})
        return jsonify({'message': f'Reading for {datetime_str} deleted successfully'}), 200
    except Exception as ex:
        return jsonify({'error': str(ex)}), 500

# ------------------------------------------------------------
# Run the Flask app
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True, port=5000)
