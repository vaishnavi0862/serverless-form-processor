import json
import uuid
import boto3
from datetime import datetime

# Initialize DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('FormSubmissions')

def lambda_handler(event, context):
    try:
        # Parse incoming data from API Gateway
        if 'body' in event:
            body = json.loads(event['body'])
        else:
            body = event
        
        # Extract form fields
        name = body.get('name', '')
        email = body.get('email', '')
        message = body.get('message', 'No message provided')
        
        # Validation
        if not name or not email:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Name and Email are required fields'
                })
            }
        
        # Generate unique ID for submission
        submission_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        # Store in DynamoDB
        item = {
            'submissionId': submission_id,
            'name': name,
            'email': email,
            'message': message,
            'submittedAt': timestamp,
            'status': 'processed'
        }
        
        table.put_item(Item=item)
        
        # Return success response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'success': True,
                'message': 'Form submitted successfully!',
                'submissionId': submission_id,
                'submittedAt': timestamp
            })
        }
    
    except Exception as e:
        # Error handling
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }
