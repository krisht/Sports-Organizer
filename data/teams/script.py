import requests

cookies = {
    '$com.wm.reflector': 'reflectorid:00742495493607605375@lastupd:1481398740969@firstcreate:1481398740969',
    'exp': '0%2B1481398740%2B%2B0%2B',
    'SSLB': '2',
    'account-flyout': '1',
    '_bsc-gopt': '0',
    '_tap_path': '/rum.gif',
    's_pers': '%20s_v%3DY%7C1481400545535%3B%20s_cmpstack%3D%255B%255B'aff'%252C'1481398745541'%255D%255D%7C1639165145541%3B%20gpv_p11%3DHomepage%7C1481400545542%3B%20gpv_p44%3DHomepage%7C1481400545545%3B%20s_vs%3D1%7C1481400545552%3B',
    's_sess': '%20cmp%3DF8vuM_ADID%3B%20ent%3DHomepage%3B%20cp%3DY%3B%20chan%3Daff%3B%20v59%3DHomepage%3B%20v54%3DHomepage%3B%20cps%3D1%3B%20s_sq%3D%3B',
    '_tap-criteo': '1481398744458:1481398745675:1',
    '_tap-mediamath': '1481398745674:1481398746254:1',
    '_tap-appnexus': '1481398746253:1481398746900:1',
    '_tap-turn': '1481398746900:0:1',
    's_vi': '[CS]v1|2C262CEC8507D179-60000116E000165D[CE]',
    'btc': 'b8BGRphOBZtbZvABhyoA5o',
    'bsc': 'QQZL7GSoaGsqXy8x_82yKc',
    'b30msc': 'b8BGRphOBZtbZvABhyoA5o',
    'vtc': 'b8BGRphOBZtbZvABhyoA5o',
    'bstc': 'b8BGRphOBZtbZvABhyoA5o',
}

headers = {
    'DNT': '1',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'en-US,en;q=0.8,fr;q=0.6',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36',
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Referer': 'https://www.walmart.com/?u1=ebs965597504sbe&oid=276009.10001832&wmlspartner=AysPbYF8vuM&sourceid=00742495493607605375&affillinktype=4&veh=aff',
    'Connection': 'keep-alive',
}

r = requests.get('https://beacon.walmart.com/rum.gif?athcpid=xiW7Gg-H&athpgid=athenaHomepage&athznid=athenaModuleZone&athmtid=AthenaPOVStory&athena=true&pos=0&athtype=impression&u=https%3A%2F%2Fwww.walmart.com%2F%3Fu1%3Debs965597504sbe%26oid%3D276009.10001832%26wmlspartner%3DAysPbYF8vuM%26sourceid%3D00742495493607605375%26affillinktype%3D4%26veh%3Daff&r=http%3A%2F%2Fwww.nolovenopain.com%2Fc_138a85e20b%2Faz%2Ffront.php%3Ffs%3D1%26rf%3Dwww.generatorland.com&atlznid=contentZone2&atlmtid=MultiStoryPOVResponsive&err=%7B%22act%22%3A%7B%22code%22%3A2%2C%22desc%22%3A%22Invalid%20Act%22%7D%7D&ts=1481398769166&pv_id=f0cc4aa9-e44c-4069-af1b-2b85c7435aa2&x=21&a=ATHENA_IMPRESSION&ctx=&rp=&si=uswm&sv=d.www.1.0&tv=v0&cd=%7B%22dim%22%3A%7B%22vw%22%3A0%2C%22vh%22%3A0%2C%22sw%22%3A1920%2C%22sh%22%3A1080%2C%22iw%22%3A0%2C%22ih%22%3A0%7D%7D', headers=headers, cookies=cookies)

print r.text; 