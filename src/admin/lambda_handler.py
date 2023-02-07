import json
import traceback
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.utils import get_current_week

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

def get_results():
    resp = table.query(KeyConditionExpression= Key('type').eq('admin'))
    return resp['Items'][0]['results']

def submit_results(body):
    if(get_current_week() < body['weekNum']):
        return

    week_num = body['weekNum'] - 1
    results = body['results']

    resp = table.query(KeyConditionExpression= Key('type').eq('admin'))
    curr_results = resp['Items']

    curr_results[0]['results'][week_num] = results

    table.put_item(
        Item=curr_results[0]
    )

    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
    users = resp['Items']

    for user in users:
        current_team = list(user['user_picked_teams'][week_num].keys())[0]
        if(current_team in list(results.keys())):
            user['user_picked_teams'][week_num] = {current_team: results[current_team]}

            start_streak = user['is_start_streak_alive']
            start_streak_num = 0
            total_correct_num = 0
            index = 0
            for pick in user['user_picked_teams']:
                if(index > week_num):
                    break
                val = next(iter(pick.values()))
                if(val == ''):
                    print('Skipping for now, no result is set')
                elif('Team' in next(iter(pick)) or not val):
                    start_streak = False                    
                elif(start_streak and val):
                    start_streak_num += 1
                    total_correct_num += 1
                elif(val):
                    total_correct_num += 1
                
                index += 1
            
            user['is_start_streak_alive'] = start_streak
            user['start_streak'] = start_streak_num
            user['total_correct'] = total_correct_num

            print(user)
            table.put_item(
                Item=user
            )
        else:
            user['is_start_streak_alive'] = False
            table.put_item(
                Item=user
            )


def lambda_handler(event, context):

    try:
        if(event['path'] == '/admin-submit-results'):
            print('SUBMITTING MATCHUP RESULTS')
            submit_results(json.loads(event['body']))

            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }    

        elif(event['path'] == '/admin-get-results'):
            print('GETTING MATCHUP RESULTS')
            results = get_results()

            return {
                'statusCode': 200,
                'body': json.dumps(results),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }  
    except Exception as e:
        traceback.print_exc()
        response_data = {
            'statusCode': 500,
            'error': 'Error running admin API: ' + str(e)
        }
        return response_data
