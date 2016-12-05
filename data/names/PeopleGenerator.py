# import requests

# cookies = {
#     'CFID': '32111250',
#     'CFTOKEN': '7da91ea9781d4fdd-9BF0AEF6-DE0E-18AD-D7C89F0B5805CD89',
#     '__utmt': '1',
#     '__utma': '82857099.641911703.1480307651.1480307651.1480307651.1',
#     '__utmb': '82857099.2.10.1480307651',
#     '__utmc': '82857099',
#     '__utmz': '82857099.1480307651.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
# }

# headers = {
#     'Origin': 'http://listofrandomnames.com',
#     'Accept-Encoding': 'gzip, deflate',
#     'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6',
#     'Upgrade-Insecure-Requests': '1',
#     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#     'Cache-Control': 'max-age=0',
#     'Referer': 'http://listofrandomnames.com/index.cfm?generated',
#     'Connection': 'keep-alive',
#     'DNT': '1',
# }

# data = {
#   'action': 'main.generate',
#   'numberof': '1000',
#   'nameType': 'm',
#   'fnameonly': '0',
#   'allit': '0'
# }

# r=requests.post('http://listofrandomnames.com/index.cfm?generated', headers=headers, cookies=cookies, data=data)

# f = open('Names.html', 'w'); 
# f.write(r.text); 
# f.close(); 
# 
# 
# Names from http://listofrandomnames.com/index.cfm?generated using a post request using above code

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
            if i < 20:
            	print("Coach", file = f); 
            	print(randint(100000,500000), file= f);
            elif i<500:
            	print("Athlete", file = f);
            	print(randint(150,250), file = f);
            	print(randint(65,80), file = f); 
            else: 
            	break;
            print("", file = f); 

f.close(); 