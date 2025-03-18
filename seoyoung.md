# 비행데이터 분석 

import pandas as pd
from nycflights13 import flights, planes

# 1. 출발지와 도착지별로 비행 횟수 분석 
route_counts = flights.groupby(['origin', 'dest']).size().reset_index(name='flight_count')

# 2. 비행 횟수 상위 5개 경로 출력
top_routes = route_counts.nlargest(5, 'flight_count')

# 3. 출발 시간을 시간대로 변환하여 시간대별 비행 횟수 분석
flights['hour'] = pd.to_datetime(flights['time_hour']).dt.hour
hourly_counts = flights.groupby('hour').size().reset_index(name='flight_count')
top_hours = hourly_counts.nlargest(5, 'flight_count')

# 4. 기종별 비행 횟수 분석
flights_data_with_planes = pd.merge(flights, planes, on='tailnum', how='left')
model_counts = flights_data_with_planes.groupby('model').size().reset_index(name='flight_count')
top_models = model_counts.nlargest(5, 'flight_count')

# 5. 공항별 주류 경로 추출 / 1과 코드 동일함 
route_counts = flights.groupby(['origin', 'dest']).size().reset_index(name='flight_count')

# 공항별로 묶기
route_counts_jfk = route_counts[route_counts['origin'] == 'JFK']
route_counts_lga = route_counts[route_counts['origin'] == 'LGA']
route_counts_eWR = route_counts[route_counts['origin'] == 'EWR']

# 비행 횟수 상위 5개 경로 출력
top_jfk_routes = route_counts_jfk.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')
top_lga_routes = route_counts_lga.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')
top_eWR_routes = route_counts_eWR.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')

# 6. 공항별 주류 경로에서 사용된 기종 확인 먼가 이상함
merged = pd.merge(flights, planes, on='tailnum', how='left')
# top_routes에서 상위 5개 경로만 선택
top_routes_5 = top_routes.head(5)
# 상위 5개 경로에서 사용된 기종만 필터링
top_routes_planes = merged[merged[['origin', 'dest']].apply(tuple, axis=1).isin(top_routes_5[['origin', 'dest']].apply(tuple, axis=1))]
# 결과 확인
top_routes_planes[['origin', 'dest', 'model']].drop_duplicates()


# 경로별 사용된 기종 개수 세기
route_model_count = top_routes_planes.groupby(['origin', 'dest', 'model']).size().reset_index(name='count')
route_model_count_sorted = route_model_count.sort_values(['origin', 'dest', 'count'], ascending=[True, True, False])

# 7. 공항별 가장 많이 운행된 기종 찾기
airport_top_model = merged.groupby(['origin', 'model']).size().reset_index(name='count')
airport_top_model = airport_top_model.loc[airport_top_model.groupby('origin')['count'].idxmax()]

# 8. 공항별 가장 많이 사용된 기종의 평균 좌석 수 확인
model_seat_count = planes.groupby('model')['seats'].mean().reset_index()
airport_top_model_seats = airport_top_model.merge(model_seat_count, on='model', how='left')

# 결과 출력
print("Top Routes:", top_routes)
print("Top Hours:", top_hours)
print("Top Models:", top_models)
print("Top JFK Routes:", top_jfk_routes)
print("Top LGA Routes:", top_lga_routes)
print("Top EWR Routes:", top_eWR_routes)
print("Route Model Count Sorted:", route_model_count_sorted)
print("Airport Top Model Seats:", airport_top_model_seats)
