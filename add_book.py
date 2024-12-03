import boto3
import json
import uuid


"""lambda function to post book to dynamoDB"""
# Add CORS headers to the response
def cors_response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",  # Allow all origins
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
        "body": json.dumps(body),
    }

def lambda_handler(event, context):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Name of the DynamoDB table
    table_name = "Books"
    table = dynamodb.Table(table_name)

    # Get the book data from the event
    try:
        book = json.loads(event['body'])

        # Generate a unique 'id' for the book
        book['id'] = str(uuid.uuid4())

        # Insert book into the DynamoDB table
        table.put_item(Item=book)

        # Return a success response with CORS headers
        return cors_response(201, {"message": "Book added successfully", "book": book})

    except Exception as e:
        # Print the error for debugging and return a failure response with CORS headers
        print(f"Error: {str(e)}")
        return cors_response(500, {"error": str(e)})
