import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


friends = [{'배추','옥수수'},{'당근','파'},{'오이','파'},{'시금치','감자'},{'배추','토마토'},{'당근' ,'열무'},{'콩', '배추'},{'콩', '오이'},{'콩', '옥수수' },{'콩','감자' }]

vege_list = []
for i in friends:
    vege_list.extend(i)
    
vege_list = list(set(vege_list))


rows = []
for target in vege_list:
    row = []
    for vege in vege_list:
        row.append({target,vege} in friends)
    rows.append(row)

relation_matrix = np.array(rows)

relation_matrix = pd.DataFrame(relation_matrix)
relation_matrix.columns = vege_list
relation_matrix.index = vege_list


norm = pd.read_csv(r'C:\GitHub\Supporters_monsanto\app_development_competition\재식간격.csv', engine = 'python')
norm.index = norm['작물명']
norm = norm.drop('작물명', axis = 1)

''' 실패 사례1
def design_my_farm(vege,x_max,y_max):
    vege = '시금치'
    x_max = 140
    y_max = 200
    if x_max < y_max:
        norm_coord = x_max
        norm_coord2 = y_max
    else:
        norm_coord = y_max
        norm_coord2 = x_max
    
    doodook_range = norm.loc[vege,'두둑']
    doodook_cnt = int(norm_coord / doodook_range )
    
    sep_cnt = doodook_cnt  + (doodook_cnt  -1 )
    
    residual = norm_coord - doodook_range*doodook_cnt 
    
    gorang_range = round(residual  / (sep_cnt - doodook_cnt))
    if gorang_range == np.inf:
        gorang_range = 0
    sep = []
    while (1):
        sep.append(doodook_range)
        if sum(sep) >= norm_coord:
            sep = sep[:-1]
            break
        sep.append(gorang_range)
        if sum(sep) >= norm_coord:
            break
    
    line_range = norm.loc[vege,'줄간격']
    line_cnt = int(doodook_range / line_range)
    
    
    residual = doodook_range - line_range*(line_cnt-1) 
    residual_range = residual/2
    
    doodook_sep = []
    doodook_sep.append(residual_range)
    while (1):
        if sum(doodook_sep) >= doodook_range-residual_range:
            break
        doodook_sep.append(line_range)
    doodook_sep.append(residual_range)
    
    first_coord = []
    tmp = 0
    for idx,i in enumerate(sep):
        if i == doodook_range:
            cnt = 0
            for j in doodook_sep:
                cnt += 1
                tmp += j
                if cnt != len(doodook_sep):
                    first_coord.append(tmp)
        else:
            tmp += gorang_range
            
    pogi_range = int(norm_coord2 / norm.loc[vege,'포기간격'])
    second_coord = list(range(pogi_range,norm_coord2 , pogi_range ))
    
    
    x_coord = []
    y_coord = []
    for i in first_coord:
        x_coord.extend(np.repeat(i,len(second_coord)))
        y_coord.extend(second_coord)
    
    import matplotlib.pyplot as plt
    from matplotlib import font_manager, rc
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    
    plt.figure(figsize=((norm_coord/norm_coord2)*10, 10))
    plt.xlim(0,norm_coord)
    plt.ylim(0,norm_coord2)
    plt.title(vege)
    plt.scatter(x_coord, y_coord)
    plt.show()

design_my_farm('시금치',140,200)
'''

## 두둑에 먼저 채우고  고랑 간격에 맞게 두둑을 옯기는 방향으로!!
## 지금은 두둑위치를 만들고 두둑을 채우는 것과 반대로~! 
## 1단계 주어진 텃밭에서 (어떤)가로*(어떤)세로 두둑이 만들어 지는 지를 파악한다.
## 두둑의 수는 최소화하는 방향으로 (두둑 만들기 힘드니까 ㅠㅠ)
## 2단계 두둑을 포기간격, 줄간격에 맞게 채운다.
## 1단계를 활용해서 두득을 정렬한다. 


# 작은 게 x # 큰게 y 무조건. 
x = 120
y = 100
vege = '시금치'

def doodook(x,y,vege): 
    pogi = norm.loc[vege,'포기간격']
    line = norm.loc[vege,'줄간격']
    x_cnt = int((x-1)/pogi)
    y_cnt = int((y-1)/line)
    
    x_coord = []
    residual = (x - pogi*(x_cnt))/2
    
    x_coord.append(residual)
    for i in range(x_cnt):
        tmp = residual+pogi*(i+1)
        x_coord.append(tmp)
    
    x_coord.append(x_coord[-1]+residual)
    
    y_coord = []
    residual = (y - line*(y_cnt))/2
    
    y_coord.append(residual)
    for i in range(y_cnt):
        tmp = residual+line*(i+1)
        y_coord.append(tmp)
    y_coord.append(y_coord[-1]+residual)
    
    x_coord[:-1]
    y_coord[:-1]
    
    
    x_s = []
    y_s = []
    for i in x_coord[:-1]:
        x_s.extend(np.repeat(i,len(y_coord[:-1])))
        y_s.extend(y_coord[:-1]) 
    
    import matplotlib.pyplot as plt
    from matplotlib import font_manager, rc
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    
    plt.figure(figsize=((x/y)*10, 10))
    plt.xlim(0,x)
    plt.ylim(0,y)
    plt.title(vege)
    plt.scatter(x_s, y_s)
    plt.show()
    
    return x_s, y_s

x_s, y_s = doodook(70,300,'감자')


# 작은게 무조건 wide

wide = 300
long = 500
vege1 = '시금치'
vege2 = '옥수수'

def my_farm(wide, long, vege1, vege2 = vege1, minimum_gorang_range = 10):
    doodook_range1 = norm.loc[vege1]['두둑']
    doodook_range2 = norm.loc[vege2]['두둑']
    
    if doodook_range1 + doodook_range2 > wide + minimum_gorang_range:
        doodook_side = long
        follow_side = wide
    else: 
        doodook_side = wide
        follow_side = long
    
    p_d_cnt_vege1 = doodook_side // (doodook_range1+minimum_gorang_range+10)
    p_d_cnt_vege2 = doodook_side // (doodook_range2+minimum_gorang_range+10) 
    
    np.array(range(1,p_d_cnt_vege1+1))
    np.array(range(1,p_d_cnt_vege2+1))
    
    candidate = doodook_range1*np.array(range(1,p_d_cnt_vege1+1))+doodook_range2*np.array(range(1,p_d_cnt_vege2+1)).reshape(p_d_cnt_vege2,1)
    
    d_cnt_vege1 = np.where(candidate == candidate[candidate < doodook_side].max())[1][0]+1
    d_cnt_vege2 = np.where(candidate == candidate[candidate < doodook_side].max())[0][0]+1
    
    residual = doodook_side - (d_cnt_vege1*doodook_range1 + d_cnt_vege2*doodook_range2)
    residual_range = residual/ (d_cnt_vege1 + d_cnt_vege2 - 1)
    
    doodook_sep = [0]
    seeds = []
    for i in range(d_cnt_vege1):
        doodook_sep.append(doodook_range1+doodook_sep[-1])
        doodook_sep.append(residual_range+doodook_sep[-1])
        seeds.append(doodook(doodook_range1,follow_side,vege1))
        
    for j in range(d_cnt_vege2):
        doodook_sep.append(doodook_range2+doodook_sep[-1])
        doodook_sep.append(residual_range+doodook_sep[-1])
        seeds.append(doodook(doodook_range2,follow_side,vege2))
        
    doodook_sep = doodook_sep[:-1]
    
    plt.figure(figsize=((doodook_side /follow_side)*10, 10))
    plt.xlim(0,doodook_side )
    plt.ylim(0,follow_side)
    plt.title(vege1 + ' ' +  vege2)
    
    for idx, i in enumerate(doodook_sep):
        plt.plot([i for x in range(-100,long+100,10)],range(-100,long+100,10),c = 'black')
        if idx % 2 == 0:
            plt.scatter([x+i for x in seeds[idx//2][0]],seeds[idx//2][1])
    
    plt.show()


my_farm(300,500,'오이','감자') 

