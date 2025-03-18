import pandas as pd
from nycflights13 import flights, planes

pd.DataFrame(planes)

# 1. 출발지/도착지 별 비행 횟수 분석 / 주류 경로 추출 가능
route_counts = flights.groupby(['origin', 'dest']).size().reset_index(name='flight_count')
route_counts

# 2. 비행 횟수 상위 5개 경로 출력
top_routes = route_counts.nlargest(5, 'flight_count')
top_routes

# 3. 기종별 비행 횟수 분석
merged = pd.merge(flights, planes, on='tailnum', how='left')

model_counts = merged.groupby('model').size().reset_index(name='flight_count')
top_models = model_counts.nlargest(5, 'flight_count')

# 4. 공항별로 묶기
route_counts_jfk = route_counts[route_counts['origin'] == 'JFK']
route_counts_lga = route_counts[route_counts['origin'] == 'LGA']
route_counts_eWR = route_counts[route_counts['origin'] == 'EWR']

# 5. 비행 횟수 상위 5개 경로 출력
top_jfk_routes = route_counts_jfk.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')
top_lga_routes = route_counts_lga.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')
top_eWR_routes = route_counts_eWR.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')

# 6. 상위 5개 경로에서 사용된 기종만 필터링
top_routes_planes = merged[merged[['origin', 'dest']].apply(tuple, axis=1).isin(top_routes[['origin', 'dest']].apply(tuple, axis=1))]
top_routes_planes

top_routes_planes[['origin', 'dest', 'model']].drop_duplicates()

# 7. 경로별 사용된 기종 개수 세기
route_model_count = top_routes_planes.groupby(['origin', 'dest', 'model']).size().reset_index(name='count')
route_model_count_sorted = route_model_count.sort_values(['origin', 'dest', 'count'], ascending=[True, True, False])
route_model_count_sorted

# 8. 공항별 가장 많이 운행된 기종 찾기
airport_top_model = merged.groupby(['origin', 'model']).size().reset_index(name='count')
airport_top_model = airport_top_model.loc[airport_top_model.groupby('origin')['count'].idxmax()]
airport_top_model

# 9. 공항별 가장 많이 사용된 기종의 평균 좌석 수 확인
model_seat_count = planes.groupby('model')['seats'].mean().reset_index()
airport_top_model_seats = airport_top_model.merge(model_seat_count, on='model', how='left')
airport_top_model_seats

# 10. 장/단거리 노선별 비행 분석
merged['air_time'].isna().sum()    # 결측치 확인 9430 개
merged['air_time']    # 336776개 (결측치가 2.8퍼센트 정도 = 걍 결측치 제거해버리기로)

air_time_data = merged['air_time'].dropna() # 결측치 제거

q1 = air_time_data.quantile(0.25)  # 25% 분위수
q2 = air_time_data.median()        # 50% (중앙값)
q3 = air_time_data.quantile(0.75)  # 75% 분위수

short_distance_threshold = q1  # 단거리 기준(25%)
long_distance_threshold = q3   # 장거리 기준(75%)

# 거리 구분해주는 함수 작성
def distance(air_time):
    if air_time <= short_distance_threshold:
        return "단거리"
    elif air_time >= long_distance_threshold:
        return "장거리"
    else:
        return "중거리"
    
# 11. 공항별 평균 비행시간 계산
airport_avg_air_time = merged.groupby('origin')['air_time'].mean().reset_index(name='avg_air_time')

# 12. 공항별 평균 거리 계산 (비행시간 기준으로 거리 구분)
merged['distance_category'] = merged['air_time'].apply(distance)

# 13. 공항별로 거리 구분된 비행의 평균 비행시간 계산
airport_distance_avg_air_time = merged.groupby(['origin', 'distance_category'])['air_time'].mean().reset_index(name='avg_air_time')
airport_avg_air_time, airport_distance_avg_air_time

combined = pd.merge(airport_avg_air_time, airport_distance_avg_air_time, on='origin')



# 14. 항공사별로 거리 유형에 따른 기종 사용 횟수 계산
distance_plane_counts = merged.groupby(['origin', 'distance_category', 'model']).size().reset_index(name='plane_count')

# 15. 각 거리 유형별로 기종 사용 횟수를 내림차순으로 정렬
distance_plane_counts_sorted = distance_plane_counts.sort_values(by=['distance_category', 'plane_count'], ascending=[True, False])
distance_plane_counts_sorted

# 16. 거리별로 선호하는 기종 보기
short_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['distance_category'] == '단거리']
medium_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['distance_category'] == '중거리']
long_distance_planes = distance_plane_counts_sorted[distance_plane_counts_sorted['distance_category'] == '장거리']

# 결과 출력
print("단거리 선호 기종:")
print(short_distance_planes)

print("\n중거리 선호 기종:")
print(medium_distance_planes)

print("\n장거리 선호 기종:")
print(long_distance_planes)





# 3. 출발 시간을 시간대로 변환하여 시간대별 비행 횟수 분석
# flights['hour'] = pd.to_datetime(flights['time_hour']).dt.hour
# hourly_counts = flights.groupby('hour').size().reset_index(name='flight_count')
# top_hours = hourly_counts.nlargest(5, 'flight_count')

