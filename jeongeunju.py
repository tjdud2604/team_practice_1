# filghts 데이터 분석 및 시각화
# 주제 자유:
# merge 사용해서 flight와 planes 병합한 데이터롱 각 데이터 변수 최소 하나씩 분석
# 날짜&시간 전처리 코드 들어갈 것
# 문자열 전처리 코드 들어갈 것
# 시각화 종류 최소 3가지 사용(배우지 않은것도 가능)


# 3가지 항공사에서 사용할 비행기 구매 전략 수립

# 3개 공항 >> 어떤 공항에 대한 구매전략 

# 코스 / 주 운행시간 / 목적지 / 기종 / 시트(이용객) / 




# 코스 : 공항별 주류코스
# >>> 출발공항 / 도착공항 / 운행 횟수 / 시트 수

# 주 운행시간
# >>> 시간, 공항, 기종/시트 수




# 우리가 가지 않는 도착공항 (다른 항공사에서는 많이 이용하는) 사용할지 선정
# >> 만약에 우리가 선정한 공항에서 사용하지않는 도착지가 있는지 
# 있다면, 그곳을 사용하는 것이 어떨지 >> 초점 맞춘 공항에 비주류 코스가 하나 더 생기는 것


 # 기종별 운영횟수
# 항공사 별 선호 기종
# 단거리 장거리에 주로 쓰이는 기종


from nycflights13 import flights, planes
import pandas as pd
flights.info()
planes.info()
flights['flight']


import pandas as pd
from nycflights13 import flights, planes

# flights와 planes 데이터를 tailnum 기준으로 병합
merged = pd.merge(flights, planes, how='left', on='tailnum')



# JFK 공항 출발 기준으로 필터링
jfk_flights = merged[merged['origin'] == 'JFK']


# 1. JFK 공항의 노선별 운행 횟수, 시트 수 
jfk_info = jfk_flights.groupby(['origin','dest']).agg(   # 도차지로 그룹바이
    flight_count=('flight', 'size'),   # 운행횟수
    total_seat=('seats', 'sum')       # 해당 노선의 좌석 수
).reset_index()

jfk_info['avg_seat_per_flight'] = jfk_info['total_seat'] / jfk_info['flight_count']
jfk_info_sorted = jfk_info.sort_values(by='flight_count', ascending=False)    # flight_count 기준 내림정렬

# jfk 공항 기준 주요 노선(운행횟수 순)
print(jfk_info_sorted.head(10))



# 2. JFK 공항 출발 기준 출발 및 도착 지연 분석
delay_data = jfk_flights.groupby(['origin','dest']).agg(
    total_dep_delay=('dep_delay', 'sum'),
    total_arr_delay=('arr_delay', 'sum'),
    avg_dep_delay=('dep_delay', 'mean'),
    avg_arr_delay=('arr_delay', 'mean')
).reset_index()

delay_data_sorted = delay_data.sort_values(by='avg_dep_delay', ascending=False)   #avg_dep_delay 기준 내림차순

# JFK 공항 기준 평균 출발 지연이 긴 노선
print(delay_data_sorted.head(10))


# 3. JFK 공항에서 출발하는 장거리 & 단거리 비행 분석

# 결측치 확인
merged['air_time'].isna().sum()    # 9430 개
merged['air_time']    # 336776개 (결측치가 2.8퍼센트 정도 = 걍 결측치 제거해버리기로)

# 결측치 제거
air_time_data = merged['air_time'].dropna()

# 분위수 계산
q1 = air_time_data.quantile(0.25)  # 25% 분위수
q2 = air_time_data.median()        # 50% (중앙값)
q3 = air_time_data.quantile(0.75)  # 75% 분위수



# 데이터 기반 거리 기준 설정
short_distance_threshold = q1  # 단거리 기준(25%)
long_distance_threshold = q3   # 장거리 기준(75%)

# 0 ~ 25% : 단거리
# 25% ~ 75%: 중거리
# 75% ~ : 장거리


# 거리 구분해주는 함수 작성
def distance(air_time):
    if air_time <= short_distance_threshold:
        return "단거리"
    elif air_time >= long_distance_threshold:
        return "장거리"
    else:
        return "중거리"
    

# 공항별 평균 비행시간, 거리 계산
jfk_distance_info = jfk_flights.groupby(['origin','dest']).agg(
    avg_air_time=('air_time', 'mean'),
    avg_distance=('distance', 'mean')
).reset_index()

# 위에서 만든 함수 apply해서 단거리/중거리/장거리 구분하기
jfk_distance_info['flight_type'] = jfk_distance_info['avg_air_time'].apply(distance)
print(jfk_distance_info.info())




# 4. JFK 공항에서 수익성이 높은 노선 분석
# 뭘 기준으로하지..... 수익석을 생각할 때 좌석수(seats)/운행횟수(fligth_count) 등을 사용할 수 있을 듯
# 1) 많은 좌석 + 많은 운행 횟수 = 수익성이 높을 가능성이 크다
# 2) 비행 시 평균좌석수를 분석 = 같은 운행횟수라도 좌석이 많은 비행이 수익성이 높을 수 있다(운행 효율)
# 3) 그냥 운행 횟수를 기준으로? = 많이 운행할수록 수익성이 높을 가능성이 있음
jfk_combined = pd.merge(jfk_info, jfk_distance_info, on=['origin', 'dest'])


# 1) 많은 좌석 + 많은 운행 횟수 기준
jfk_combined['seat_per_flight'] = jfk_combined['total_seat'] / jfk_combined['flight_count']

# 좌석 수 * 운행 횟수 기준으로 수익성 높은 노선 도출
jfk_combined['seat_flight_product'] = jfk_combined['total_seat'] * jfk_combined['flight_count']

# seat_flight_product 기준으로 내림차순 정렬
revenue_seat_flight = jfk_combined.sort_values(by='seat_flight_product', ascending=False)
revenue_seat_flight.head(10)


# 2) 평균 좌석 수 기준
jfk_combined['avg_seat_per_flight'] = jfk_combined['total_seat'] / jfk_combined['flight_count']

# 평균 좌석 수 기준으로 내림차순 정렬
revenue_avg_seat = jfk_combined.sort_values(by='avg_seat_per_flight', ascending=False)


#---------뭔가 분석해보고싶었는데 망한 것 같습니다-------------

# 거리별(단거리/중거리/장거리) 선호 비행기 모델
# 거리 정보가 포함된 jfk_distance_info에서 'flight_type' (단거리, 중거리, 장거리)과 기종 정보를 활용
# JFK 공항에서 출발하는 비행기의 기종과 거리별 사용 횟수 분석
jfk_flights_with_distance = pd.merge(jfk_flights, jfk_distance_info[['origin', 'dest', 'flight_type']], 
                                     how='left', on=['origin', 'dest'])

# 거리별로 기종 사용 횟수 계산
distance_plane_counts = jfk_flights_with_distance.groupby(['flight_type','model']).size().reset_index(name='plane_count')

# 거리별로 많이 사용된 기종 정렬
distance_plane_counts_sorted = distance_plane_counts.sort_values(by='plane_count', ascending=False)

# 거리별로 기종 사용 횟수를 계산한 후, 각 거리 유형별로 정렬
distance_plane_counts_sorted = distance_plane_counts.sort_values(by=['flight_type', 'plane_count'], ascending=[True, False])

# 단거리, 중거리, 장거리별로 구분해서 보기
short_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['flight_type'] == '단거리']
medium_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['flight_type'] == '중거리']
long_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['flight_type'] == '장거리']

print(short_distance_planes.head(10))
print(medium_distance_planes.head(10))
print(long_distance_planes.head(10))

