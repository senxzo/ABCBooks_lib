import boto3
import json

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

    # Get the ID from the event
    try:
        book_id = event.get('pathParameters', {}).get('id')
        if not book_id:
            return cors_response(400, {"error": "ID is required to delete a book"})

        # Debugging: Print the ID to check what's being passed
        print(f"Received ID: {book_id}")

        # Verify the book exists
        response = table.get_item(Key={'id': book_id})

        # Debugging: Print the response to check if the book exists
        print(f"GetItem response: {response}")

        # If 'Item' is not in the response, the book doesn't exist
        if 'Item' not in response:
            return cors_response(404, {"error": "Book not found"})

        # Delete the book if it exists
        delete_response = table.delete_item(Key={'id': book_id})

        # Debugging: Print the delete response
        print(f"DeleteItem response: {delete_response}")

        # Return success message after deletion
        return cors_response(200, {"message": "Book deleted successfully"})

    except Exception as e:
        # Print and return any exception errors
        print(f"Error: {str(e)}")
        return cors_response(500, {"error": str(e)})
