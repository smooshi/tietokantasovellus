#Tällä tiedostolla vaan populoidaan databaseen nopeasti jotain että voi sitten sörkkiä jos joutuu sen pyyhkimään

import app
from app.models import *
from app.notes import *
from datetime import datetime

#Kolme käyttäjää
insert_user("Milla", "email@email.com", "test", False)
insert_user("Tommi", "email2@email.com", "test", False)
insert_user("Elina", "email3@email.com", "test", False)

#Noteja def insert_note(user_id, text, isTimed, time, date):
time = datetime.now()
date = datetime.now().date()
insert_note(1, "Millan eka", False, time, date)
insert_note(1, "Millan toka", False, time, date)
insert_note(1, "Millan kolmas", False, time, date)
insert_note(2, "Tommin eka", False, time, date)
insert_note(2, "Tommin toka", False, time, date)
insert_note(3, "Elinan eka", False, time, date)
