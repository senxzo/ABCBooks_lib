def lambda_handler(event, context):
    import boto3
    import json
    
    """Lambda function to edit items in dynamoDB using serverless Architechture"""

    # Initialize DynamoDB resource
    dynamodb = boto3.resource("dynamodb")
    table_name = "Books"
    table = dynamodb.Table(table_name)

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

    try:
        # Log incoming event for debugging
        print("Received event:", json.dumps(event))

        # Extract the 'id' from the URI path parameters
        book_id = event["pathParameters"].get("id")

        if not book_id:
            return cors_response(400, {"error": "Book ID is required in the URI"})

        # Parse the body from the event
        book = json.loads(event.get("body", "{}"))

        # Validate if required fields are provided in the body
        if not all(key in book for key in ["Title", "Authors", "Publisher", "Year"]):
            return cors_response(400, {"error": "Missing required fields in the request body"})

        # Use ExpressionAttributeNames to map reserved keyword 'Year' to a placeholder
        expression_attribute_names = {"#yr": "Year"}

        # Update the book in DynamoDB
        table.update_item(
            Key={"id": book_id},  # Use the book_id from the URI as the key
            UpdateExpression="SET Title = :title, Authors = :authors, Publisher = :publisher, #yr = :year",
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues={
                ":title": book["Title"],
                ":authors": book["Authors"],
                ":publisher": book["Publisher"],
                ":year": book["Year"],
            },
            ReturnValues="UPDATED_NEW",
        )

        return cors_response(200, {"message": "Book updated successfully", "book": book})

    except Exception as e:
        print(f"Error: {str(e)}")
        return cors_response(500, {"error": str(e)})
