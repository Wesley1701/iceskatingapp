import sqlite3


class Track:

    def __init__(self, id: int, name: str, city: str, country: str, outdoor: bool, altitude: int) -> None:
        self.id = id
        self.name = name
        self.city = city
        self.country = country
        self.outdoor = outdoor
        self.altitude = altitude

    # Representation method
    # This will format the output in the correct order
    # Format is @dataclass-style: Classname(attr=value, attr2=value2, ...)
    def __repr__(self) -> str:
        return "{}({})".format(type(self).__name__, ", ".join([f"{key}={value!s}" for key, value in self.__dict__.items()]))

    # Makes sure we can confirm if two tracks have the same values inside them
    def __eq__(self, other) -> bool:
        return self.id == other.id and self.name == other.name and self.city == other.city and self.country == other.country and self.outdoor == other.outdoor and self.altitude == other.altitude

    # returns a list of Event’s for this track
    def get_events(self, db="iceskatingapp.db"):
        from event import Event
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(f'SELECT * FROM events WHERE track_id = "{self.id}"')
        events = c.fetchall()
        event_list = []
        for e in events:
            ev = Event(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
            event_list.append(ev)
        conn.commit()
        c.close()
        conn.close()
        return event_list
