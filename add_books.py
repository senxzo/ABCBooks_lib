import boto3
import json
import uuid


"""Lambda script to add an array of books into dynamoDB"""

def lambda_handler(event, context):
    # Initialize DynamoDB resource
    dynamodb = boto3.resource('dynamodb')

    # Name of the DynamoDB table
    table_name = "Books"
    table = dynamodb.Table(table_name)

    # The book data to upload
    books = [
        {
            "Title": "Automating DevOps with GitLab CI/CD Pipelines",
            "Authors": "Christopher Cowell, Nicholas Lotz and Chris Timberlake",
            "Publisher": "Packt Publishing",
            "Year": 2023
        },
        {
            "Title": "AWS Cookbook",
            "Authors": "John Culkin and Mike Zazon",
            "Publisher": "O'Reilly Media",
            "Year": 2021
        },
        {
            "Title": "Serverless Development on AWS",
            "Authors": "Sheen Brisals and Luke Hedger",
            "Publisher": "O'Reilly Media",
            "Year": 2024
        },
        {
            "Title": "Building Scalable Apps with Redis and Node.js",
            "Authors": "Joshua Johanan",
            "Publisher": "Packt Publishing",
            "Year": 2014
        },
        {
            "Title": "Terraform Cookbook",
            "Authors": "Kerim Satirli and Taylor Dolezal",
            "Publisher": "O'Reilly Media",
            "Year": 2024
        },
        {
            "Title": "Amazon Web Services in Action",
            "Authors": "Michael Wittig and Andreas Wittig",
            "Publisher": "Manning Publications",
            "Year": 2023
        }
    ]

    # Insert books into the DynamoDB table
    try:
        for book in books:
            # Add a unique 'id' to each book using UUID
            book['id'] = str(uuid.uuid4())  # Generate a unique id for each book
            table.put_item(Item=book)
            print(f"Uploaded: {book['Title']}")
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Books uploaded successfully!"})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
