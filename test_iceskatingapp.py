from skater import Skater
from event import Event
from track import Track

from datetime import datetime
import pytest

skater = Skater(18, "Jan", "Blokhuijsen", "NED", "M", datetime(1984, 4, 1))
track = Track(24, "Thialf", "Heerenveen", "NED", 0, 3)
event = Event(1,"Essent ISU World Cup - 1500m Men Division A", 29, datetime(2003, 11, 8), 1500,  107.37, 3, "Nuis", "M")


# Test to check if the age of a skater is correct based on the date_of_birth
def test_age_of_skater():
    assert skater.get_age() == 39


# Test to check if the amount of events for a specific skater is returned correctly
def test_amount_of_events_of_skater():
    assert len(skater.get_events()) == 3


# Test to check if the amount of events for a specific track is returned correctly
def test_amount_of_events_of_track():
    assert len(track.get_events()) == 20


# Test to check if the returned date matches the specified format for that event date
def test_event_date_conversion():
    assert event.convert_date("%Y-%m-%d") == "2003-11-08"


# Test to check if the duration is converted from 1H19 to the specified format
def test_event_duration_conversion():
    assert event.convert_duration("%M:%S") == "01:47"


# Test to check the amount of skaters on a specified event
def test_amount_of_skaters_on_event():
    assert len(event.get_skaters()) == 56


# Test to validate if the given track of a specified event is correct
def test_track_on_event():
    assert event.get_track() == Track(29, "Hamar Olympic Hall", "Hamar", "NOR", False, 123)
