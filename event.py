import sqlite3

from skater import Skater
from track import Track
from datetime import timedelta, datetime


class Event:

    def __init__(self, id: int, name: str, track_id: int, date: datetime, distance: str, duration: float, laps: int, winner: str, category: str) -> None:
        self.id = id
        self.name = name
        self.track_id = track_id
        self.date = date
        self.distance = distance
        self.duration = duration
        self.laps = laps
        self.winner = winner
        self.category = category

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))

    # adds skater to event table event_skaters via the id of the passed skater object and the id of this event
    def add_skater(self, skater, db="iceskatingapp.db") -> None:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        ins = 'INSERT INTO event_skaters (skater_id, event_id) VALUES (?, ?)'
        c.execute(f'SELECT * FROM event_skaters where skater_id = {skater.id} AND event_id = {self.id}')
        es = c.fetchall()
        if len(es) == 0:
            c.execute(ins, (skater.id, self.id))
        conn.commit()
        c.close()
        conn.close()

    # returns a list of Skaters
    # search in table event_skaters for all skater_id’s on this event, search all skaters with those id’s
    def get_skaters(self, db="iceskatingapp.db") -> list[Skater]:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        skater_list = []
        c.execute(f'SELECT skater_id FROM event_skaters WHERE event_id = "{self.id}"')
        skaters = c.fetchall()
        for skater in skaters:
            c.execute(f'SELECT * FROM skaters WHERE id = "{skater[0]}"')
            e = c.fetchall()[0]
            s = Skater(e[0], e[1], e[2], e[3], e[4], e[5])
            skater_list.append(s)
        conn.commit()
        c.close()
        conn.close()
        return skater_list

    # returns Track object
    def get_track(self, db="iceskatingapp.db") -> Track:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        track = ""
        c.execute(f'SELECT * FROM tracks WHERE id = "{self.track_id}"')
        track = c.fetchall()[0]
        track = Track(track[0], track[1], track[2], track[3], track[4], track[5])
        c.close()
        conn.close()
        return track

    # returns converted date of this event in the provided datetime format
    def convert_date(self, to_format) -> str:
        converted_date = self.date.strftime(to_format)
        return converted_date

    # returns converted duration in the provided datetime format
    def convert_duration(self, to_format) -> str:
        duration = timedelta(seconds=self.duration)
        dt = datetime.strptime(str(duration), "%H:%M:%S.%f")
        converted_duration = dt.strftime(to_format)
        return converted_duration
