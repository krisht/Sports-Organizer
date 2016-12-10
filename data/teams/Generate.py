import requests

cookies = {
    '_ga': 'GA1.2.949152876.1480309731',
    '_gat': '1',
}

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
    'Accept': '*/*',
    'Referer': 'http://www.mithrilandmages.com/utilities/CityNames.php',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
}

r=requests.get('http://www.mithrilandmages.com/utilities/CityNamesServer.php?count=50&dataset=united_states&_=1480309731235', headers=headers, cookies=cookies)

f = open('towns.html', 'w'); 
f.write(r.text); 
f.close(); 