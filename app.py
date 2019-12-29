import sqlite3
import os
from flask import g, Flask, render_template
import datetime

app = Flask(__name__)
DATABASE = os.environ.get('AIRODUMP_DB_FILE')
TABLE_NAME = os.environ.get('AIRODUMP_TABLE_NAME', 'whoiswalkingby')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def minutes_ago(number_of_minutes):
    time_difference = datetime.datetime.now() - datetime.timedelta(minutes=number_of_minutes)
    return str(time_difference)

def query_thirty_minutes_ago(cursor):
    thirty_minutes_ago = minutes_ago(30)
    query = 'SELECT * from %s WHERE last_seen > "%s" AND '\
            'number_packets < %s ORDER BY last_seen DESC' % (TABLE_NAME, thirty_minutes_ago, 500)
    return cursor.execute(query).fetchall()

def query_new_clients_in_day(cursor):
    a_day_ago = minutes_ago(1440)
    query = 'SELECT * from %s WHERE first_seen > "%s" AND '\
            'number_packets < %s ORDER BY last_seen DESC' % (TABLE_NAME, a_day_ago, 50)
    return cursor.execute(query).fetchall()

def count_query(cursor):
    query = 'SELECT COUNT(*) from %s WHERE probed_essids != ""' % (TABLE_NAME)
    return cursor.execute(query).fetchone()

def oldest_query(cursor):
    query = 'SELECT MIN(first_seen) from %s' % (TABLE_NAME)
    return cursor.execute(query).fetchone()

@app.route('/')
def index():
    cursor = get_db().cursor()
    all_results = query_thirty_minutes_ago(cursor)
    passerby_list = query_new_clients_in_day(cursor)
    count = count_query(cursor)
    oldest_date = oldest_query(cursor)
    return render_template('whoiswalkingby.html',
                           all_results=all_results,
                           passerby_list=passerby_list,
                           count=count,
                           oldest_date=oldest_date)
