
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
