from nycflights13 import flights , planes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 3가지 항공사에서 사용할 비행기 구매 전략 

# 3개 공항 >> 어떤 공항에 대한 구매전략 

# 코스 / 주 운행시간 / 목적지 / 기종 / 시트(이용객) / 




# 코스 : 공항별 주류코스
# >>> 출발공항 / 도착공항 / 운행 횟수 / 시트 수

# 주 운행시간
# >>> 시간, 공항, 기종/시트 수



planes.info()
# 우리가 가지 않는 도착공항 (다른 항공사에서는 많이 이용하는) 사용할지 선정
# >> 만약에 우리가 선정한 공항에서 사용하지않는 도착지가 있는지 
# 있다면, 그곳을 사용하는 것이 어떨지 >> 초점 맞춘 공항에 비주류 코스가 하나 더 생기는 것


merged = pd.merge(flights,planes,how='left',on='tailnum')
merged['time_hour'] = pd.to_datetime(merged['time_hour'])
merged.info()
def airport (x):
    # 해당 공항 주로 운행하는 도착지 상위 5개
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

    # 주중 주간으로 나누기
    def week_select(x):
        if x>4:
            return True
        else:
            return False
    airport_mainstream['week'] = airport_mainstream['time_hour'].dt.weekday.apply(week_select)
    airport_mainstream_weekday = airport_mainstream.loc[airport_mainstream['week']==0]
    airport_mainstream_weekend = airport_mainstream.loc[airport_mainstream['week']==1]

    # 주중 공항별 시간별 Delay 시간
    airport_mainstream_weekday_need =airport_mainstream_weekday.pivot_table(
    index=['dest','hour'],
    values='dep_delay',
    aggfunc='mean'
    ).reset_index()
    # 주말 공항별 시간별 Delay 시간
    airport_mainstream_weekend_need =airport_mainstream_weekend.pivot_table(
    index=['dest','hour'],
    values='dep_delay',
    aggfunc='mean'
    ).reset_index()
    return airport_mainstream_distance , airport_mainstream_weekday_need ,airport_mainstream_weekend_need
# 도착지별로 거리는 (단거리,장거리) 이므로 (단거리,장거리)용 항공기를 배치해야하고 (주중,주간)에 (시간)이 혼잡하기 때문에 seat수가 많은 비행기를 배치하여 혼잡도를 줄일 필요가 있다.
jfk_mainstream_distance , jfk_mainstream_weekday_need ,jfk_mainstream_weekend_need = airport("JFK")

# 시간별 (단거리 장거리 , 항공사 , 시트 수) 가 delay와 어느정도 연관성이 있는지에 대한 정보

plt.figure(figsize=(10, 6))
sns.lineplot(data=jfk_mainstream_weekday_need, x='hour', y='dep_delay', hue='dest', marker='o')
# 주 운행시간
# >>> 시간, 공항, 기종/시트 수




# 우리가 가지 않는 도착공항 (다른 항공사에서는 많이 이용하는) 사용할지 선정
# >> 만약에 우리가 선정한 공항에서 사용하지않는 도착지가 있는지 
# 있다면, 그곳을 사용하는 것이 어떨지 >> 초점 맞춘 공항에 비주류 코스가 하나 더 생기는 것