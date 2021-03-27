# put your python code here
journey_duration = int(input())
journey_duration_minus_one = journey_duration - 1
food_cost_per_day = int(input())
total_food_cost = food_cost_per_day * journey_duration
one_way_flight_cost = int(input())
total_flight_cost = one_way_flight_cost * 2
one_night_in_hotel_cost = int(input())
total_hotel_cost = one_night_in_hotel_cost * journey_duration_minus_one
result = total_food_cost + total_flight_cost + total_hotel_cost
print(result)
