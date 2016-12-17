from __future__ import print_function;
sqlFile = open('teams.sql', 'w+'); 

def mascot(name, mascot):
    print('INSERT INTO TeamMascot VALUES ("%s", "%s");' % (name, mascot), file=sqlFile); 

def team(tid, name, hometown):
    print('INSERT INTO Team VALUES (%s, "%s", "%s");' % (tid, name, hometown), file=sqlFile);  

f1 = open('mascots.txt')
f2 = open('towns.txt')
f3 = open('schools.txt')

mascots = [line.strip() for line in f1 if line.strip() != ""]
towns = [line.strip() for line in f2 if line.strip() != ""]
schools = [line.strip() for line in f3 if line.strip() != ""]
f1.close()
f2.close()
f3.close()


for i, (m, s) in enumerate(zip(mascots, schools)):
    mascot('%s' % s,'%s'% m)


c = 0
while len(schools) < 350:
    schools.append(schools[c])
    c += 1

c = 0
while len(towns) < 350:
    towns.append(towns[c])
    c += 1

for i, (s, t) in enumerate(zip(schools, towns)):
    team(i+1, '%s' % s, t)