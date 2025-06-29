import json
import boto3
import random
import string

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ShortURLs')  # ← Confirm this matches your table name

def lambda_handler(event, context):
    # Parse input (JSON or plain text)
    if isinstance(event.get('body'), str):
        try:
            body = json.loads(event['body'])
            long_url = body.get('url', '')
        except:
            long_url = event['body']
    else:
        long_url = event.get('body', {}).get('url', '')
    
    # Generate short code
    short_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    
    # Save to DynamoDB
    table.put_item(Item={
        'short_code': short_code,
        'long_url': long_url
    })
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'short_url': f'https://chvsmruvq6.execute-api.us-east-1.amazonaws.com/dev/{short_code}'
        })
    }
