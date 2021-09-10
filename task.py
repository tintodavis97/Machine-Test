import pandas as pd
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians


df = pd.read_csv('latitude_longitude_details.csv')
df = df[df['longitude'] < 76.4]
df = df[df['latitude'] < 12]
# df.drop_duplicates(keep=False, inplace=True)

# # Ŷ = b0 + b1*x

# first 
# x_dash = mean(x)
# y_dash = mean(y)
    
# second
# x_x_dash = (x-x_dash)
# y_y_dash = (y-y_dash)

# third
# x_x_dash_sq = x_x_dash**2
# x_x_dash_sq_sum = sum(x_x_dash_sq)

# xy_dash = x_x_dash*y_y_dash
# xy_dash_sum = sum(xy_dash)

# fourth
# # Ŷ = b0 + b1*x
# b1 = xy_dash_sum/x_x_dash_sq_sum
# x = x_x_dash
# Ŷ = y_dash
# b0 = Ŷ-b1*x
# y = mx + c


# x = df['latitude']
# y = df['longitude']

x_dash = df.mean()['latitude']
y_dash = df.mean()['longitude']

# x1 = x[x[0]-x_dash]
df['x_x_dash'] = df['latitude'] - x_dash
df['y_y_dash'] = df['longitude'] - y_dash
df['x_x_dash_sq'] = df['x_x_dash']**2
x_x_dash_sq_sum = sum(df['x_x_dash_sq'])
df['xy_dash'] = df['x_x_dash'] * df['y_y_dash']
xy_dash_sum = sum(df['xy_dash'])

b1 = xy_dash_sum/x_x_dash_sq_sum
# y = mx + c
# c = y - mx
b0 = y_dash - b1*x_dash
# y = mx + c
# -mx+y-c=0
c=b0
m=b1
df['x'] = df['latitude']
df['y'] = df['latitude'] * m + b0

plt.plot(df['x'], df['y'], color='r')
plt.plot(df['latitude'], df['longitude'], color='g')
plt.show()



m1 = -(1/m)
# y = mx + c
# y_ = m1x + c1
# c1 = y_ - m1x

# y_ = m1*df['latitude'] + c1
df['c1'] = df['longitude'] - (m1 * df['latitude'])

# y - m1x - c1 = 0
# y - mx - c = 0
# y - m1x - c1 = y - mx - c
# -m1x - c1 = -mx - c
# mx - m1x = c1 - c
# x(m-+m1) = c1 - c
# x = (c1 - c)/(m - m1)

df['x_'] = (df['c1'] - c)/(m - m1)
df['y_'] = m1 * df['x_'] + df['c1']

R = 6373.0

for i, row in df.iterrows():
    lat1 = radians(row['x'])
    lon1 = radians(row['y'])
    lat2 = radians(row['x_'])
    lon2 = radians(row['y_'])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    con = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    origin = (row['latitude'], row['longitude'])
    dist = (row['x_'], row['y_'])
    distence_ = R * con
    
    df.loc[i, 'distance'] = distence_
    terrain = {'0':'boundary wall,road', '.5':'road', '1.5': 'river side', '3': 'civil station, road'}
    
    min_val = abs(float('0') - distence_)
    terrain_index = '0'
    for j in terrain.keys():
        if abs(float(j) - distence_) < min_val:
            terrain_index = j
    df.loc[i, 'terrain'] = terrain[terrain_index]
df = df.drop(['x_x_dash', 'y_y_dash', 'x_x_dash_sq', 'xy_dash', 'c1', 'x_', 'y_'], axis=1)
df = df[df['terrain'].str.contains('road')]
df = df[~(df['terrain'].str.contains('civil station'))]
df
