from __future__ import print_function; 

from random import randint; 

i = 0; 

f = open('people.txt', 'w'); 

with open('firsts.txt') as firsts:
    with open('lasts.txt') as lasts:
        for i, line in enumerate(firsts):
            first = line.split()[0].title()
            last = lasts.next().split()[0].title()
            full =  "%s %s" % (first, last)
            print(full, file = f); 
            print("%s.%s@gmail.com" % (first.lower(), last.lower()), file = f); 
            print("abc123", file = f);
            if i < 100:
            	print("Coach", file = f); 
            	print(randint(100000,500000), file= f);
            elif i<5000:
            	print("Athlete", file = f);
            	print(randint(150,250), file = f);
            	print(randint(65,80), file = f); 
            else: 
            	break;
            print("", file = f); 

f.close(); 