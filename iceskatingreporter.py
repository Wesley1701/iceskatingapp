from track import Track
from event import Event
from skater import Skater
from datetime import datetime
import sqlite3
import csv


class Reporter:
    def menu(self):
        option = ""
        while option != "X":
            print('Reporter Testing')
            print('[0] Get total amount of skaters')
            print('[1] Get highest track')
            print('[2] Get longest and shortest event')
            print('[3] Get events with most laps for track')
            print('[4] Get skaters with most events')
            print('[5] Get tracks with most events')
            print('[6] Get first event')
            print('[7] Get latest event')
            print('[8] Get skaters that skated on track between two dates')
            print('[9] Get tracks in country')
            print('[10] Get skaters with nationality')
            print('[X] Exit')
            option = input('Write the number of the option you want to test: ')
            options = [self.total_amount_of_skaters, self.highest_track, self.longest_and_shortest_event, self.events_with_most_laps_for_track, self.skaters_with_most_events, self.tracks_with_most_events]
            if option in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
                if option == "3":
                    while True:
                        t_id = input("Please enter the track id you want to check: ")
                        if t_id.isnumeric():
                            print(self.events_with_most_laps_for_track(int(t_id)))
                            break
                        else:
                            print("Please enter a valid id")
                elif option == "4":
                    while True:
                        only_wins = input("Do you want to only count the wins? (Y/N): ")
                        if only_wins == "Y":
                            print(self.skaters_with_most_events(True))
                            break
                        elif only_wins == "N":
                            print(self.skaters_with_most_events(False))
                            break
                        else:
                            print("Invalid option, please try again")
                elif option == "6" or option == "7":
                    outside = ""
                    while outside != 'X' and outside != 'Y':
                        outside = input("If you want to search only the outside tracks type 'Y' else type 'X': ")
                        if outside == 'Y':
                            if option == 6:
                                res = self.get_first_event(True)
                            else:
                                res = self.get_latest_event(True)
                        elif outside == 'X':
                            if option == 6:
                                res = self.get_first_event(False)
                            else:
                                res = self.get_latest_event(False)
                        else:
                            print("Invalid option, please try again")
                    print(res)
                elif option == "8":
                    tracks = [
                        Track(15, "Thialf", "Collalbo", "ITA", 1, 1198),
                        Track(22, "Alau Ice Palace", "Nur-Sultan", "KAZ", 0, 350),
                        Track(24, "Thialf", "Heerenveen", "NED", 0, 3),
                        Track(24, "Hamar Olympic Hall", "Hamar", "NOR", 0, 123),
                        Track(24, "Uralskaya Molniya", "Chelyabinsk", "RUS", 0, 220),
                        Track(24, "Utah Olympic Oval", "Salt Lake City", "USA", 0, 1425)
                    ]
                    print("Please pick a track you want to use for this search")
                    print("[0] Ritten Arena")
                    print("[1] Alau Ice Palace")
                    print("[2] Thialf")
                    print("[3] Hamar Olympic Hall")
                    print("[4] Uralskaya Molniya")
                    print("[5] Utah Olympic Oval")
                    x = input("Track: ")
                    while x not in ['0', '1', '2', '3', '4', '5']:
                        print("Invalid option, please try again")
                        x = input("Track: ")
                    track = tracks[int(x)]
                    while True:
                        print("Start date:")
                        start = self.date_input()
                        print("End date:")
                        end = self.date_input()
                        if start < end:
                            break
                        print("Start date is after end date please try again")
                    while True:
                        to_csv = input("Do you want to create a csv file? (Y/N): ")
                        if to_csv == "Y":
                            res = self.get_skaters_that_skated_track_between(track, start, end, True)
                            break
                        elif to_csv == "N":
                            res = self.get_skaters_that_skated_track_between(track, start, end, False)
                            break
                        else:
                            res = "Invalid option, please try again"
                    print(res)
                elif option == "9":
                    country = input("Enter the country code (ex. NED, USA, etc.) you would like to see the tracks from: ")
                    while True:
                        to_csv = input("Do you want to create a csv file? (Y/N): ")
                        if to_csv == "Y":
                            res = self.get_tracks_in_country(country, True)
                            break
                        elif to_csv == "N":
                            res = self.get_tracks_in_country(country)
                            break
                        else:
                            print("Invalid option, please try again")
                    if res != ():
                        print(res)
                    else:
                        print("No tracks found in this country")
                elif option == "10":
                    nation = input("Enter the country code (ex. NED, USA, etc.) you would like to see the skaters from: ")
                    while True:
                        to_csv = input("Do you want to create a csv file? (Y/N): ")
                        if to_csv == "Y":
                            res = self.get_skaters_with_nationality(nation, True)
                            break
                        elif to_csv == "N":
                            res = self.get_skaters_with_nationality(nation)
                            break
                        else:
                            print("Invalid option, please try again")
                    if res != ():
                        print(res)
                    else:
                        print("No skaters found from this country")
                else:
                    print(options[int(option)]())
                input('Press enter to continue')
            elif option == "X":
                print('Exiting program...')
            else:
                print('Invalid option, please try again')

    # Create a date from an input
    def date_input(self) -> datetime:
        date_format = '%Y-%m-%d'
        while True:
            date_in = input("Date (format should be 'YYYY-MM-DD'): ")
            try:
                date_object = datetime.strptime(date_in, date_format)
                return date_object
            except ValueError:
                print('Invalid date or incorrect data format(should be YYYY-MM-DD)')

    # How many skaters are there? -> int
    def total_amount_of_skaters(self) -> int:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM skaters')
        skaters = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return len(skaters)

    # What is the highest track? -> Track
    def highest_track(self) -> Track:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM tracks ORDER BY altitude DESC LIMIT 1')
        tracks = c.fetchall()[0]
        highest_track = Track(tracks[0], tracks[1], tracks[2], tracks[3], tracks[4], tracks[5])
        conn.commit()
        c.close()
        conn.close()
        return highest_track

    # What is the longest and shortest event? -> tuple[Event, Event]
    def longest_and_shortest_event(self) -> tuple[Event, Event]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'select * from events ORDER BY duration ')
        events = c.fetchall()
        shortest = Event(events[0][0], events[0][1], events[0][2], events[0][3], events[0][4], events[0][5], events[0][6], events[0][7], events[0][8])
        longest = Event(events[-1][0], events[-1][1], events[-1][2], events[-1][3], events[-1][4], events[-1][5], events[-1][6], events[-1][7], events[-1][8])
        conn.commit()
        c.close()
        conn.close()
        return longest, shortest

    # Which event has the most laps for the given track_id -> tuple[Event, ...]
    def events_with_most_laps_for_track(self, track_id: int) -> tuple[Event, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM tracks WHERE id = {track_id}')
        tracks = c.fetchall()
        if len(tracks) == 0:
            return None
        track = tracks[0]
        track = Track(track[0], track[1], track[2], track[3], track[4], track[5])
        events = track.get_events()
        most_laps = 0
        most_track = tuple()
        for event in events:
            if event.laps > most_laps:
                most_laps = event.laps
                most_track = (event, )
            elif event.laps == most_laps:
                most_track += (event, )
        conn.commit()
        c.close()
        conn.close()
        return most_track

    # Which skaters have made the most events -> tuple[Skater, ...]
    # Which skaters have made the most succesful events -> tuple[Skater, ...]
    def skaters_with_most_events(self, only_wins: bool = False) -> tuple[Skater, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM skaters')
        skaters = c.fetchall()
        count = 0
        most_events = tuple()
        if only_wins:
            for skater in skaters:
                s = Skater(skater[0], skater[1], skater[2], skater[3], skater[4], skater[5])
                if len(s.get_wins()) > count:
                    count = len(s.get_wins())
                    most_events = (s, )
                elif len(s.get_wins()) == count:
                    most_events += (s, )
        else:
            for skater in skaters:
                s = Skater(skater[0], skater[1], skater[2], skater[3], skater[4], skater[5])
                if len(s.get_events()) > count:
                    count = len(s.get_events())
                    most_events = (s, )
                elif len(s.get_events()) == count:
                    most_events += (s, )
        conn.commit()
        c.close()
        conn.close()
        return most_events

    # Which track has the most events -> Track
    def tracks_with_most_events(self) -> tuple[Track, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM tracks')
        tracks = c.fetchall()
        most_events = tuple()
        count = 0
        for track in tracks:
            t = Track(track[0], track[1], track[2], track[3], track[4], track[5])
            if len(t.get_events()) > count:
                count = len(t.get_events())
                most_events = (t,)
            elif len(t.get_events()) == count:
                most_events += (t,)
        c.close()
        conn.close()
        return most_events

    # Which track had the first event? -> Event
    # Which track had the first outdoor event? -> Event
    def get_first_event(self, outdoor_only: bool = False) -> Event:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        if outdoor_only:
            c.execute(f'SELECT id FROM tracks where outdoor=1')
            tracks = c.fetchall()
            track_ids = tuple(tracks) if len(tracks) != 1 else "(" + str(tracks[0][0]) + ")"
            c.execute(f'SELECT * FROM events WHERE track_id in {track_ids} ORDER BY date')
            e = c.fetchone()
        else:
            c.execute(f'SELECT * FROM events ORDER BY date')
            e = c.fetchone()
        first = Event(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
        c.close()
        conn.close()
        return first

    # Which track had the latest event? -> event
    # Which track had the latest outdoor event? -> event
    def get_latest_event(self, outdoor_only: bool = False) -> Event:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        if outdoor_only:
            c.execute(f'SELECT id FROM tracks WHERE outdoor=1')
            tracks = c.fetchall()
            track_ids = tuple(tracks) if len(tracks) != 1 else "(" + str(tracks[0][0]) + ")"
            c.execute(f'SELECT * FROM events WHERE track_id in {track_ids} ORDER BY date DESC')
            e = c.fetchone()
        else:
            c.execute(f'SELECT * FROM events ORDER BY date DESC')
            e = c.fetchone()
        last = Event(e[0], e[1], e[2], e[3], e[4], e[5], e[6], e[7], e[8])
        c.close()
        conn.close()
        return last

    # Which skaters have raced track Z between period X and Y? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters on Track Z between X and Y.csv`
    # example: `Skaters on Track Kometa between 2021-03-01 and 2021-06-01.csv`
    # date input always in format: YYYY-MM-DD
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_that_skated_track_between(self, track: Track, start: datetime, end: datetime, to_csv: bool = False) -> tuple[Skater, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM events WHERE track_id = {track.id}')
        events = c.fetchall()
        skater_ids = set()
        skaters = tuple()
        if to_csv:
            skaters += (('id', 'first_name', 'last_name', 'nationality', 'gender', 'date_of_birth'), )
        for event in events:
            date = datetime.strptime(event[3], "%Y-%m-%d")
            if start <= date <= end:
                c.execute(f'SELECT skater_id FROM event_skaters where event_id = {event[0]}')
                ids = c.fetchall()
                for item in ids:
                    if item[0] not in skater_ids:
                        skater_ids.add(item[0])
                        c.execute(f'SELECT * FROM skaters WHERE id = {item[0]}')
                        skater = c.fetchone()
                        if not to_csv:
                            skater = Skater(skater[0], skater[1], skater[2], skater[3], skater[4], skater[5])
                        skaters += (skater, )
        if to_csv:
            filename = f'Skaters on Track {track.name} between {start.strftime("%Y-%m-%d")} and {end.strftime("%Y-%m-%d")}.csv'
            with open(filename, 'w') as fin:
                cout = csv.writer(fin)
                cout.writerows(skaters)
        c.close()
        conn.close()
        return skaters

    # Which tracks are located in country X? ->tuple[Track, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Tracks in country X.csv`
    # example: `Tracks in Country USA.csv`
    # otherwise it should just return the value as tuple(Track, ...)
    # CSV example (this are also the headers):
    #   id, name, city, country, outdoor, altitude
    def get_tracks_in_country(self, country: str, to_csv: bool = False) -> tuple[Track, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM tracks WHERE country = "{country}"')
        tracks = c.fetchall()
        tracks_in_country = tuple()
        if len(tracks) <= 0:
            return tracks_in_country
        if to_csv:
            tracks_in_country += (('id', 'name', 'city', 'country', 'outdoor', 'altitude'),)
            for track in tracks:
                tracks_in_country += (track,)
            filename = f'Tracks in Country {country}.csv'
            with open(filename, 'w') as fin:
                cout = csv.writer(fin)
                cout.writerows(tracks_in_country)
        tracks_in_country = tuple()
        for track in tracks:
            t = Track(track[0], track[1], track[2], track[3], track[4], track[5])
            tracks_in_country += (t, )
        c.close()
        conn.close()
        return tracks_in_country

    # Which skaters have nationality X? -> tuple[Skater, ...]
    # Based on given parameter `to_csv = True` should generate CSV file as  `Skaters with nationality X.csv`
    # example: `Skaters with nationality GER.csv`
    # otherwise it should just return the value as tuple(Skater, ...)
    # CSV example (this are also the headers):
    #   id, first_name, last_name, nationality, gender, date_of_birth
    def get_skaters_with_nationality(self, nationality: str, to_csv: bool = False) -> tuple[Skater, ...]:
        conn = sqlite3.connect('iceskatingapp.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM skaters WHERE nationality = "{nationality}"')
        skaters = c.fetchall()
        skaters_with_nationality = tuple()
        if len(skaters) <= 0:
            return skaters_with_nationality
        if to_csv:
            skaters_with_nationality += (('id', 'name', 'city', 'country', 'outdoor', 'altitude'),)
            for skater in skaters:
                skaters_with_nationality += (skater,)
            filename = f'Skaters with nationality {nationality}.csv'
            with open(filename, 'w') as fin:
                cout = csv.writer(fin)
                cout.writerows(skaters_with_nationality)
        skaters_with_nationality = tuple()
        for skater in skaters:
            s = Skater(skater[0], skater[1], skater[2], skater[3], skater[4], skater[5])
            skaters_with_nationality += (s,)
        c.close()
        conn.close()
        return skaters_with_nationality
