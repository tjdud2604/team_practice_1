
merged = pd.merge(flights, planes, on='tailnum', how='left')

# JFK 공항 정리
# 1. 주류 경로 추출 위한 코드 / 선호 루트
route_counts = flights.groupby(['origin', 'dest']).size().reset_index(name='flight_count')
route_counts
route_counts_jfk = route_counts[route_counts['origin'] == 'JFK']

top_routes = route_counts.nlargest(5, 'flight_count')
top_routes
top_jfk_routes = route_counts_jfk.sort_values(by='flight_count', ascending=False).nlargest(5, 'flight_count')
top_jfk_routes

# 2. 선호 루트 기종 확인
top_routes_planes = merged[merged[['origin', 'dest']].apply(tuple, axis=1).isin(top_routes[['origin', 'dest']].apply(tuple, axis=1))]
top_routes_planes

route_model_count = top_routes_planes.groupby(['origin', 'dest', 'model']).size().reset_index(name='count')
route_model_count_sorted = route_model_count.sort_values(['origin', 'dest', 'count'], ascending=[True, True, False])
route_model_count_sorted

# JFK 공항만 필터링
jfk_routes_model_count = route_model_count_sorted.loc[route_model_count_sorted['origin'] == 'JFK']
jfk_routes_model_count

# 3. JFK 피크타임 확인
airport_hourly_flights = flights.groupby(['origin', 'hour']).size().reset_index(name='flight_count')
airport_hourly_flights

jfk_airport_hourly_flights = airport_hourly_flights.loc[airport_hourly_flights['origin'] == 'JFK']
jfk_airport_hourly_flights

# 피크타임 top 5
top_hourly_JFK = jfk_airport_hourly_flights.nlargest(5, 'flight_count')
top_hourly_JFK

# 특정 기종을 많이 운항하는 항공사 찾기
carrier_model_flights = merged.groupby(['carrier', 'model']).size().reset_index(name='flight_count')
carrier_model_flights

# JFK 공항 피크타임 분석
airport_hourly_flights = flights.groupby(['origin', 'hour']).size().reset_index(name='flight_count')
airport_hourly_flights

# JFK 공항 데이터 필터링
jfk_airport_hourly_flights = airport_hourly_flights.loc[airport_hourly_flights['origin'] == 'JFK']



# 시간대별 평균 비행 횟수 계산
average_flight_count = jfk_airport_hourly_flights['flight_count'].mean()
average_flight_count

# 평균보다 적은 비행 횟수인 시간대 찾기
low_flight_times = jfk_airport_hourly_flights[jfk_airport_hourly_flights['flight_count'] < average_flight_count]
low_flight_times

# 특정 시간대에 비행을 운항하는 항공사 찾기
# 항공사별 시간대별 비행 횟수 분석
carrier_hourly_flights = flights.groupby(['carrier', 'origin', 'hour']).size().reset_index(name='flight_count')

# 평균보다 적은 비행 횟수를 운항하는 시간대와 공항
low_flight_times = jfk_airport_hourly_flights[jfk_airport_hourly_flights['flight_count'] < jfk_airport_hourly_flights['flight_count'].mean()]

# 평균보다 적은 비행 횟수를 운항하는 항공사 찾기
low_flight_time_airlines = pd.merge(low_flight_times, carrier_hourly_flights, on=['origin', 'hour'], how='inner')

# 결과 출력
low_flight_time_airlines


# 평균 기종 운항 횟수 계산
average_model_count = jfk_routes_model_count['count'].mean()

# 평균보다 적게 운항하는 기종 찾기
low_flight_models = jfk_routes_model_count[jfk_routes_model_count['count'] < average_model_count]
low_flight_models

# 특정 기종을 많이 운항하는 항공사 찾기
carrier_model_flights = merged.groupby(['carrier', 'model']).size().reset_index(name='flight_count')

# 평균보다 적은 기종을 많이 운항하는 항공사 찾기
low_flight_model_airlines = pd.merge(low_flight_models, carrier_model_flights, on='model', how='inner')
low_flight_model_airlines = low_flight_model_airlines[low_flight_model_airlines['flight_count'] > 0]
low_flight_model_airlines
