import json
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.utils import get_current_week

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

def get_results():
    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('admin'))
        print(resp["Items"])
        return resp["Items"][0]["results"]
    except Exception as e:
        raise Exception("Unable to get matchups with error: " + str(e))

# performance gap... do not submit until after deadline. Anything with "Team" indicates a no pick and a loss
def submit_results(body):
    if(get_current_week() < body["weekNum"]):
        print("Saving you a headache :)")
        return

    week_num = body["weekNum"] - 1
    results = body["results"]

    print(week_num)
    print(results)

    try:
        resp = table.query(KeyConditionExpression= Key('type').eq('admin'))
        curr_results = resp["Items"]
        print(curr_results)

        curr_results[0]["results"][week_num] = results

        table.put_item(
            Item=curr_results[0]
        )

        resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
        users = resp["Items"]

        for user in users:
            if(not user["username"] == 'mrosenbaum15'):
                print("Testing only with myself")
                continue
            print("29")
            print(user["user_picked_teams"][week_num])
            current_team = list(user["user_picked_teams"][week_num].keys())[0]
            print(32)
            print(current_team)
            if(current_team in list(results.keys())):
                print("Result found for this week")
                user["user_picked_teams"][week_num] = {current_team: results[current_team]}

                start_streak = user["is_start_streak_alive"]
                start_streak_num = 0
                total_correct_num = 0
                index = 0
                for pick in user["user_picked_teams"]:
                    if(index > week_num):
                        print("Breaking at ")
                        print(index)
                        break
                    val = next(iter(pick.values()))
                    if(val == ''):
                        print("Skipping for now, no result is set")
                    elif("Team" in next(iter(pick)) or not val):
                        print("47")
                        print(val)
                        print("User didn't submit team in time or were wrong")
                        start_streak = False                    
                    elif(start_streak and val):
                        print("Keeping ss, add 1")
                        start_streak_num += 1
                        total_correct_num += 1
                    elif(val):
                        total_correct_num += 1
                    
                    index += 1
                
                user["is_start_streak_alive"] = start_streak
                user["start_streak"] = start_streak_num
                user["total_correct"] = total_correct_num

                print(user)
                table.put_item(
                    Item=user
                )
            else:
                print("THIS USER HASN'T SUBMITTED THEIR PICK")
                print(user)

        # return ""
    except Exception as e:
        raise Exception("Unable to get matchups with error: " + str(e))


def lambda_handler(event, context):
    print(event)
    print("RETURNING 200")
    
    matchups = []
    if(event["path"] == "/admin-submit-results"):
        print("SUBMITTING MATCHUP RESULTS")
        submit_results(json.loads(event["body"]))

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }    

    elif(event["path"] == "/admin-get-results"):
        print("GETTING MATCHUP RESULTS")
        results = get_results()

        return {
            "statusCode": 200,
            "body": json.dumps(results),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": '*'
            }
        }  

