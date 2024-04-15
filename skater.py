from datetime import timedelta, datetime
import sqlite3


class Skater:

    def __init__(self, id: int, first_name: str, last_name: str, nationality: str, gender: str, date_of_birth: datetime) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.nationality = nationality
        self.gender = gender
        self.date_of_birth = date_of_birth

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))

    # returns the age in years from a specific date/or today
    def get_age(self, date=datetime.now()) -> int:
        delta = date - self.date_of_birth
        age = delta.total_seconds() / 3600 / 24 / 365.2425
        return int(age)

    # returns a list of Event’s
    def get_events(self, db="iceskatingapp.db"):
        from event import Event
        conn = sqlite3.connect(db)
        c = conn.cursor()
        event_list = []
        c.execute(f'SELECT event_id FROM event_skaters WHERE skater_id = {self.id}')
        events = c.fetchall()
        for evnt in events:
            c.execute(f'SELECT * FROM events WHERE id = "{evnt[0]}"')
            e = c.fetchall()[0]
            ev = Event(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
            event_list.append(ev)
        conn.commit()
        c.close()
        conn.close()
        return event_list

    # returns a list of Events where the skater won
    def get_wins(self, db="iceskatingapp.db"):
        from event import Event
        conn = sqlite3.connect(db)
        c = conn.cursor()
        event_list = []
        c.execute(f'SELECT event_id FROM event_skaters WHERE skater_id = "{self.id}"')
        events = c.fetchall()
        for evnt in events:
            c.execute(f'SELECT * FROM events WHERE id = "{evnt[0]}" and winner = "{self.last_name}"')
            es = c.fetchall()
            if len(es) != 0:
                e = es[0]
                ev = Event(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
                event_list.append(ev)
        conn.commit()
        c.close()
        conn.close()
        return event_list
