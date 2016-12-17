from __future__ import print_function;
from random import choice

sqlFile = open('sports.sql', 'a+'); 

sport =['Football', 'Basketball', 'Baseball', 'Soccer', 'Water Polo', 'Track', 'Cross Counry', 'Swimming', 'Rugby', 'Tennis']; 

seasons = ['Fall', 'Winter', 'Spring' , 'Summer']; 

sports = []

for s in sport:
	for season in seasons:
		sports.append((s, season)); 

position = ["Forward", "Center", "Back", "Left", "Right", "Goalie"]

days = map(str, range(1,29))
months = ["%02d" % ii for ii in range(1, 13) ]; 
years  = ["%04d" % ii for ii in range(2009, 2017)]


def circular(list):
	ii = 0; 
	while True:
		yield list[ii]
		ii = (ii+1) % len(list)

def numbers(list):
	ii = 1; 
	jj = 0; 
	while True:
		while j < len(list):
			jj+=1; 
			yield ii; 
		ii+=1; 
		jj= 0; 


def insert_sports(name, season):
    print('INSERT INTO SportSeason VALUES ("%s", "%s");' % (name, season), file=sqlFile); 
    print('INSERT INTO Sport(name) VALUES ("%s");' % (name) , file=sqlFile); 

def insert_plays(team_id, sport_id):
    print('INSERT INTO plays VALUES (%s, %s);' % (sport_id, team_id) , file=sqlFile); 

def insert_member_of(uid, tid, number, pos):
    print('INSERT INTO member_of VALUES (%s, %s, "%s", %s);' % (uid, tid,
                                                                pos, number) , file=sqlFile); 

def insert_coaches(uid, tid):
    date = '%s-%s-%s' % (choice(years), choice(months), choice(days))
    print('INSERT INTO coaches VALUES (%s, %s, "%s");' % (uid, tid, date) , file=sqlFile); 


map(insert_sports, sports); 

tid = circular(range(1, 351))
team_numbers = numbers(range(1, 351))

pos = circular(position); 

for uid in range(101, 5001):
	insert_member_of(uid, tid.next(), team_numbers.next(), pos.next())

sid = circular(range(1,101)); 
cs = circular(range(1,101)); 
for tid in range(1, 351):
	insert_plays(tid, sid.next()); 
	insert_coaches(cs.next(), tid); 
