from nycflights13 import flights , planes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

merged = pd.merge(flights,planes,how='left',on='tailnum')
merged['time_hour'] = pd.to_datetime(merged['time_hour'])
def airport (x):
    merged_Airport = merged.loc[merged['origin']==x]
    airport_dest = merged_Airport.pivot_table(
    index='dest',
    values='flight',
    aggfunc='count'
    ).reset_index()
    airport_dest= airport_dest.sort_values("flight",ascending=False)

    # 공항에서 주류로 사용하는 5개 루트 뽑기
    airport_mainstream = merged_Airport[merged_Airport['dest'].isin(airport_dest.head(5)["dest"])]
    airport_mainstream_distance = airport_mainstream.groupby('dest')["air_time"].mean()

    def week_select(x):
        if x>4:
            return True
        else:
            return False
    airport_mainstream['week'] = airport_mainstream['time_hour'].dt.weekday.apply(week_select)
    airport_mainstream_weekday = airport_mainstream.loc[airport_mainstream['week']==0]
    airport_mainstream_weekend = airport_mainstream.loc[airport_mainstream['week']==1]

    airport_mainstream_weekday_need =airport_mainstream_weekday.pivot_table(
    index=['dest','hour'],
    values='dep_delay',
    aggfunc='mean'
    ).reset_index()

    airport_mainstream_weekend_need =airport_mainstream_weekend.pivot_table(
    index=['dest','hour'],
    values='dep_delay',
    aggfunc='mean'
    ).reset_index()
    return airport_mainstream_distance , airport_mainstream_weekday_need ,airport_mainstream_weekend_need

a,b,c = airport("JFK")