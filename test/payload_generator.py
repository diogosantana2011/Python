from jsonschema import validate, ValidationError
import json, uuid, datetime, random, math
from datetime import timezone

# schema = {
#    "type":"object",
#    "properties":{
#         "id":{
#             "type":"string"
#         },
#         "paymentType":{
#             "type":"string"
#         },
#         "paymentHandleToken":{
#             "type":"string"
#         },
#         "merchantRefNum":{
#             "type":"string"
#         }
#     }
# }

# def generate_payment_handle_payload():
#     """
#     Generate a payload for payment handles.
#     """
#     # Generate UUIDs
#     neteller_uuid = uuid.uuid4()
#     payment_handle_token = uuid.uuid4()

#     # Get current time (UTC)
#     now_utc = datetime.datetime.now(timezone.utc)
#     formatted_time = now_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

#     RETURN_LINKS = [
#         {"rel": "on_completed", "href": "https://jenkins.3et.com/manageFunding/neteller/success"},
#         {"rel": "on_failed", "href": "https://jenkins.3et.com/manageFunding/neteller/error"},
#         {"rel": "default", "href": "https://jenkins.3et.com/manageFunding"}
#     ]
    
#     response={
#         "id": str(neteller_uuid),
#         "paymentType":"NETELLER",
#         "paymentHandleToken": str(payment_handle_token),
#         "merchantRefNum":"65eb1f34-5728-4d8b-a315-618d05a2133c",
#         "currencyCode": "EUR",
#         "dupCheck": True,
#         "status": "INITIATED",
#         "liveMode":True,
#         "usage":"SINGLE_USE",
#         "action":"REDIRECT",
#         "executionMode":"SYNCHRONOUS",
#         "amount": random.randint(0, 99999),
#         "billingDetails":{
#             "street": "123 Street",
#             "street2":"Avenue",
#             "city": "",
#             "zip": "",
#             "country": ""
#         },
#         "customerIp": "",
#         "timeToLiveSeconds": random.randint(111, 999),
#         "gatewayResponse":{
#             "orderId": f"ORD_{str(uuid.uuid4())}",
#             "totalAmount": random.randint(111, 999),
#             "currency": "EUR",
#             "status":"pending",
#             "lang":"en_US",
#             "processor":"NETELLER"
#         },
#         "neteller":{
#             "consumerId": "test_dsantana",
#             "detail1Description": "Test description",
#             "detail1Text": "Test description"
#         },
#         "returnLinks":RETURN_LINKS,
#         "txnTime": formatted_time,
#         "updatedTime": formatted_time,
#         "statusTime": formatted_time,
#         "links":[
#             {
#                 "rel":"redirect_payment",
#                 "href":"https://jenkins.3et.com/manageFunding/neteller/success"
#             }
#         ]
#     }

#     return response
 
# try:
#     validate(instance={
#         "id": "string",
#         "paymentType": "48.66",
#         "paymentHandleToken": "string",
#         "merchantRefNum": "string"}, schema=schema)
#     print('Validation success')
# except ValidationError:
#       print('Validation fail')

################################################## TEST
# Multiple odds
def odds_adjustment_calculation(odds, adjustment=None):
    """
        Perform adjustment calculation for odds given to fnc.
        @reference: [Odds ajustment](https://ns90ltd.atlassian.net/wiki/spaces/3C/pages/4405657625/Multiples+price+source+adjustment+values)
        @param `odds`: list of odds, OR individual odds value. I.E; [1.737, 1.815, 1.892, 1.039, 2.560] or 1.98
            -- type: float
        @param `adjustment`: value representing % of adjustment to be made to odds (or list of odds)
            -- type: int
            
            -- if no adjustment passed, odds will be summed up.
    """
    if adjustment is None:
        return sum(odds)
    if isinstance(odds, list):
        adjusted_odds = [(odds_value - 1) * (100 - adjustment) / 100 + 1 for odds_value in odds]
        product_of_adjusted_odds = math.prod(adjusted_odds)
        return product_of_adjusted_odds
    else:
        return (odds - 1) * (100 - adjustment) / 100 + 1

def build_payload_for_multiple_bets(data, adjustment=None):
    """
        Build multiple offer payload.
        @param `data`- payload for multiple bets.
        @param `adjustment` - % adjustment for multiple odds, if any.
        @return: dict - payload modified
    """
    stake = data['bets'][0]['stake'] if 'stake' in data['bets'][0] else 200.00
    multiplier_bet_legs = data['bets'][0]['multiplierBetLegs']
    odds_list = [leg['odds'] for leg in multiplier_bet_legs]

    # Calculate adjusted odds
    multipler_odds = odds_adjustment_calculation(odds_list, adjustment)

    payload = {
        "bets": [
            {
                "multiplierBetLegs": multiplier_bet_legs,
                "stake": stake,
                "submittedType": "MULTIPLIER",
                "odds": round(multipler_odds, 4),
                "oddsType": "DECIMAL"
            }
        ],
        "platform": "euro"
    }

    return payload
################################################## TEST

payload = {
    "bets": [
        {
            "multiplierBetLegs":[
                {
                    "odds":2.36,
                    "runnerId":12716936,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds":1.8,
                    "runnerId":129428551,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds":1.2,
                    "runnerId":12942889,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds":2.98,
                    "runnerId":12710026,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds":1.80,
                    "runnerId":129488551,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds":1.62,
                    "runnerId":124328489,
                    "oddsType":"DECIMAL"
                },
                {
                    "odds": 2.36,
                    "runnerId":127169345,
                    "oddsType":"DECIMAL"
                }
            ],
            "stake": 150,
            "submittedType":"MULTIPLIER",
            "oddsType":"DECIMAL"
        }
    ],
    "platform":"euro"
}

################################################## Lottery Number picker

def generate_numbers():
    # Generate 5 unique numbers from 1 to 50
    main_numbers = random.sample(range(1, 51), 5)
    # Generate 2 unique numbers from 1 to 12
    lucky_numbers = random.sample(range(1, 13), 2)
    
    return main_numbers, lucky_numbers

# Example usage
main_numbers, lucky_numbers = generate_numbers()
print("Main Numbers:", main_numbers)
print("Lucky Numbers:", lucky_numbers)

def calculate_combinations(n, k):
    return math.comb(n, k)

total_combinations = calculate_combinations(50, 5) * calculate_combinations(12, 2)

# Format with commas as thousand separators
formatted_with_commas = f"{total_combinations:,}"

print("Total number of combinations (with commas):", formatted_with_commas)

odds_values = [1.340, 5.750, 1.610]
# print(json.dumps(build_payload_for_multiple_bets(payload, 50), indent=4))
# print(odds_adjustment_calculation(odds_values, 50))
