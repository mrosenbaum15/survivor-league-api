import json
import traceback
from datetime import datetime, timedelta
import boto3
from boto3.dynamodb.conditions import Key
from src.utils.utils import get_current_week, week_to_date_range, is_dst

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('survivor-league-db')

def setup_new_user(body):
    username = body['username']
    fullname= body['fullname']

    table.put_item(
        Item={
            'type': 'userinfo',
            'id': username,
            'username': username,
            'name': fullname,
            'user_picked_teams':  [{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''},{'Team': ''}],
            'start_streak': 0,
            'is_start_streak_alive': True,
            'latest_streak': 0,
            'total_correct': 0,
            'latest_week': 0
        }
    )

def get_curr_user_info(username):
    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
    userinfo = resp['Items'][0]

    return {
        'username': userinfo['username'],
        'fullname': userinfo['name'],
        'start_streak': int(userinfo['start_streak']),
        'total_correct': int(userinfo['total_correct']),
        'is_start_streak_alive': userinfo['is_start_streak_alive'],
        'user_picked_teams': userinfo['user_picked_teams']
    }

        
def get_curr_user_info_standings(username):
    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo') & Key('id').eq(username))
    userinfo = resp['Items'][0]
    
    week_num = get_current_week()
    sunday_of_curr_week = week_to_date_range(week_num)
    
    today = datetime.now()
    target_date = datetime.strptime(sunday_of_curr_week, '%d-%m-%Y %H:%M:%S')

    user_picks = []
    if(today < target_date and week_num > 1):
        user_picks = userinfo['user_picked_teams'][0:(week_num-1)]
    elif(today >= target_date and week_num == 1):
        user_picks.append(userinfo['user_picked_teams'][0])                          
    elif(today >= target_date):
        user_picks = userinfo['user_picked_teams'][0:week_num]                    
    
    return {
        'username': userinfo['username'],
        'fullname': userinfo['name'],
        'start_streak': int(userinfo['start_streak']),
        'total_correct': int(userinfo['total_correct']),
        'is_start_streak_alive': userinfo['is_start_streak_alive'],
        'user_picked_teams': user_picks
    }
      
def get_all_users(week_num):
    sunday_of_curr_week = week_to_date_range(week_num)
    
    today = datetime.now()
    
    target_date = datetime.strptime(sunday_of_curr_week, '%d-%m-%Y %H:%M:%S')
    
    if(today < target_date and week_num > 1):
        return {'see_users': False}                
    
    resp = table.query(KeyConditionExpression= Key('type').eq('userinfo'))
    userinfo = resp['Items']

    
    user_return = []
    for user in userinfo:
        user_return.append({user['id']: user['user_picked_teams'][int(week_num)-1]})
    return user_return




def lambda_handler(event, context):
    try:    
        if(event['path'] == '/setup-new-user'):
            code = setup_new_user(json.loads(event['body']))
            return {
                'statusCode': 201,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                }
            }    

        elif(event['path'] == '/userinfo'):
            user = get_curr_user_info(event['queryStringParameters']['user'])
            return {
                'statusCode': 200,
                'body': json.dumps(user, sort_keys=True),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    }
                }    

        elif(event['path'] == '/user-info-standings'):
            user = get_curr_user_info_standings(event['queryStringParameters']['user'])
            return {
                'statusCode': 200,
                'body': json.dumps(user, sort_keys=True),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    }
                }                

        elif(event['path'] == '/all-users'):
            users = get_all_users(event['queryStringParameters']['week_num'])
            return {
                'statusCode': 200,
                'body': json.dumps(users, sort_keys=True),
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                    }
                }       
    except Exception as e:
        traceback.print_exc()
        response_data = {
            'statusCode': 500,
            'error': 'Error running user API' + str(e)
        }
        return response_data

