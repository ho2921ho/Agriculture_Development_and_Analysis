import pandas as pd
import numpy as np

raw1 = pd.read_csv('C:\DATA\Suppoters_monsnato\전국_도별__논밭별_경지면적.csv', engine = 'python')
raw2 = pd.read_csv('C:\DATA\Suppoters_monsnato\국토면적.csv', engine = 'python')

df1 = raw1[raw1.전답별 == '계']
df1.index = df1['시도별']
df1 = df1.drop('전국', axis = 0)

df1['2017'].astype(int)

import json
import folium
import warnings
warnings.simplefilter(action = "ignore", category = FutureWarning)

geo_path = r'C:\DATA\Southkorea_maps\southkorea-maps\kostat\2013\json\skorea_provinces_geo_simple.json'
geo_str = json.load(open(geo_path, encoding = 'utf-8'))

m = folium.Map(location=[36, 127], zoom_start=7)

folium.Choropleth(
    geo_data=geo_str,
    name='choropleth',
    data= df1,
    columns=['시도별', '2018'],
    key_on='feature.name',
    fill_color='YlGn',
).add_to(m)

folium.GeoJson(geo_str).add_to(m)

m.save('C:\GitHub\Supporters_monsanto\picture\map2.html')








