from datetime import datetime, timedelta
import os
import sys
import json
import sqlite3

from skater import Skater
from iceskatingreporter import Reporter
from track import Track
from event import Event


def main():
    try:
        insert_data("events.json")
        reporter = Reporter()
        reporter.menu()
    except FileNotFoundError:
        print("No such file or directory found")


# Method that splits up the values to be put in the database
def insert_data(json_file, db_file='iceskatingapp.db'):
    with open(json_file, 'r') as file:
        data = json.load(file)
    for event in data:
        insert_events(event)
        insert_track(event['track'])
        insert_skaters(event['results'])
        insert_event_skaters(event)


# Inserts the events into the events table in the database
def insert_events(event, db_file='iceskatingapp.db'):
    # TODO: complete the method
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(f'SELECT * FROM events WHERE id = {event["id"]}')
    events = c.fetchall()
    if len(events) != 0:
        return
    ins = 'INSERT INTO events (id, name, track_id, date, distance, duration, laps, winner, category) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'
    try:
        t = datetime.strptime(event['results'][0]['time'], '%M:%S.%f')
    except ValueError:
        t = datetime.strptime(event['results'][0]['time'], '%S.%f')
    delta = timedelta(minutes=t.minute, seconds=t.second, microseconds=t.microsecond)
    e = Event(event['id'], event['title'], event['track']['id'], event['start'], event['distance']['distance'], delta.total_seconds(), event['distance']['lapCount'], event['results'][0]['skater']['lastName'], event['category'])
    c.execute(ins, (e.id, e.name, e.track_id, e.date, e.distance, e.duration, e.laps, e.winner, e.category))
    conn.commit()
    c.close()
    conn.close()


# Inserts the tracks into the tracks table in the database
def insert_track(track, db_file='iceskatingapp.db'):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    c.execute(f'SELECT * FROM tracks where id = {track["id"]}')
    tracks = c.fetchall()
    ins = 'INSERT INTO tracks (id, name, city, country, outdoor, altitude) VALUES (?, ?, ?, ?, ?, ?)'
    if len(tracks) != 0:
        return
    t = Track(track['id'], track['name'], track['city'], track['country'], track['isOutdoor'], track['altitude'])
    c.execute(ins, (t.id, t.name, t.city, t.country, t.outdoor, t.altitude))
    conn.commit()
    c.close()
    conn.close()


# Inserts the skaters into the skaters table in the database
def insert_skaters(results, db_file='iceskatingapp.db'):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    for result in results:
        c.execute(f'SELECT * FROM skaters where id = {result["skater"]["id"]}')
        skaters = c.fetchall()
        ins = 'INSERT INTO skaters (id, first_name, last_name, nationality, gender, date_of_birth) VALUES (?, ?, ?, ?, ?, ?)'
        if len(skaters) == 0:
            skater = result['skater']
            s = Skater(skater['id'], skater['firstName'], skater['lastName'], skater['country'], skater['gender'], skater['dateOfBirth'])
            c.execute(ins, (s.id, s.first_name, s.last_name, s.nationality, s.gender, s.date_of_birth))
    conn.commit()
    c.close()
    conn.close()


# Inserts the skaters that skated in an event into the event_skaters table with the ids of both in the database
def insert_event_skaters(event, db_file='iceskatingapp.db'):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    event_id = event['id']
    results = event['results']
    ins = 'INSERT INTO event_skaters (skater_id, event_id) VALUES (?, ?)'
    for result in results:
        skater_id = result['skater']['id']
        c.execute(f'SELECT * FROM event_skaters where skater_id = {skater_id} AND event_id = {event_id}')
        es = c.fetchall()
        if len(es) == 0:
            c.execute(ins, (skater_id, event_id))
    conn.commit()
    c.close()
    conn.close()


if __name__ == "__main__":
    main()
