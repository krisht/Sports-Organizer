from __future__ import print_function;
import hashlib, uuid; 
from werkzeug.security import generate_password_hash as pw_hash

salt = uuid.uuid4().hex;

sqlFile = open('people.sql', 'w'); 

def user(id, name, email, password):
	print('INSERT INTO User VALUES (%s, "%s", "%s", "%s");' % (id, name, email, password), file = sqlFile); 

def coach(uid, salary):
	print('INSERT INTO Coach VALUES (%s, %s);' % (uid, salary), file = sqlFile); 

def athlete(uid, weight, height):
	print('INSERT INTO Athlete VALUES (%s, %s, %s);' % (uid, height, weight), file = sqlFile); 

with open('people.txt') as f:
	try:
		uid = 1; 
		while True:
			name = f.next().strip(); 
			email = f.next().strip(); 
			pw = pw_hash(f.next().strip()) # Hash password later
			role = f.next().strip(); 
			user(uid, name, email, pw); 
			if role == 'Coach': 
				sal = f.next().strip(); 
				coach(uid, sal); 
			else:
				weight = f.next().strip(); 
				height = f.next().strip(); 
				athlete(uid, weight, height); 
			uid+=1; 
			f.next(); 
	except StopIteration:
		pass
		
sqlFile.close(); 