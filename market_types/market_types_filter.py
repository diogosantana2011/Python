import json

with open('market_types.json', 'r') as file:
    market_periods = json.load(file)

full_event = [markets for markets in market_periods if markets['marketPeriod'] == 'FULL_EVENT']
second_half = [markets for markets in market_periods if markets['marketPeriod'] == 'SECOND_HALF']
first_half = [markets for markets in market_periods if markets['marketPeriod'] == 'FIRST_HALF']

full_event_market_types = full_event[0]['marketTypes'] if full_event else []
second_half_market_types = second_half[0]['marketTypes'] if second_half else []
first_half_market_types = first_half[0]['marketTypes'] if first_half else []


full_event_market_type_set = set()
for market in full_event_market_types:
    full_event_market_type_set.add(market['marketType'])

second_half_market_type_set = set()
for market in second_half_market_types:
    second_half_market_type_set.add(market['marketType'])

first_half_market_type_set = set()
for market in second_half_market_types:
    first_half_market_type_set.add(market['marketType'])

full_event_unique_market_types = list(full_event_market_type_set)
print(f'Full event market types: {full_event_unique_market_types}')
print('\n')

second_half_unique_market_types = list(second_half_market_type_set)
print(f'Second half market types: {second_half_unique_market_types}')
print('\n')

first_half_unique_market_types = list(first_half_market_type_set)
print(f'First half market types: {first_half_unique_market_types}')
