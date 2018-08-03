from urllib.request import urlopen; import json; import pandas as pd

ipadd = '121.170.157.18'
geodata = pd.DataFrame(json.loads(urlopen('https://freegeoip.net/json/'+ipadd).read()), index=[0])
print(geodata.loc[0,['ip','latitude','longitude']])
