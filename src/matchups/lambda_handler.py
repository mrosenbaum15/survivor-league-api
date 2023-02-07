import json
import traceback
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

def get_all_matchups():
    resp = table.query(KeyConditionExpression= Key('type').eq('matchup') &  Key('id').eq('all'))
    return resp['Items'][0]['matchups'], resp['Items'][0]['deadlines']

def submit_user_pick(body):
    username = body['username']
    week_num = body['weekNum']
    team = body['pick'].strip()

    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
    curr_user = resp['Items'][0]

    curr_user['user_picked_teams'][week_num-1] = {team: ''}

    table.put_item(
        Item=curr_user
    )




def lambda_handler(event, context):
    try:
        matchups = []
        if(event['path'] == '/get-all-matchups'):
            matchups, deadlines = get_all_matchups()
            return_body = {
                'matchups': matchups,
                'deadlines': deadlines
            }
            return {
                'statusCode': 200,
                'body': json.dumps(return_body),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }    


        elif(event['path'] == '/submit-pick'):
            submit_user_pick(json.loads(event['body']))
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }    
    except Exception as e:
        traceback.print_exc()
        response_data = {
            'statusCode': 500,
            'error': 'Error running matchups API: ' + str(e)
        }
        return response_data


