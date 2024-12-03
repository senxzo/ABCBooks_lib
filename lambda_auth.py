import json
import jwt  # PyJWT library
import requests

def lambda_handler(event, context):
    # Extract the token from the 'Authorization' header (remove 'Bearer ' if present)
    token = event['headers'].get('Authorization', '').replace('Bearer ', '').strip()

    if not token:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized", "error": "Token is missing or invalid"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow any origin (you can set a specific origin if needed)
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allow methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization",  # Allow specific headers
            }
        }

    # Identify token type (id_token or access_token) by checking query parameters in the URL
    token_type = None
    if "id_token" in event["queryStringParameters"]:
        token_type = "id_token"
        token = event["queryStringParameters"]["id_token"]
    elif "access_token" in event["queryStringParameters"]:
        token_type = "access_token"
        token = event["queryStringParameters"]["access_token"]

    if not token_type:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized", "error": "Token type is missing"}),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow any origin
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allowed methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization"  # Allowed headers
            }
        }

    # Cognito JWK URL
    JWK_URL = "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_nWdh4ZyA0/.well-known/jwks.json"

    try:
        # Fetch JWKs
        jwks = requests.get(JWK_URL).json()

        # Decode the token using JWKs
        decoded_token = jwt.decode(
            token, 
            jwks, 
            algorithms=["RS256"], 
            audience="4i8lgashh7oblc90pr47goddei",  # Correct audience value
            options={"verify_exp": True}
        )

        # Check token type-specific claims
        if token_type == "id_token":
            if not decoded_token.get("email_verified"):
                raise Exception("Email not verified.")
        elif token_type == "access_token":
            if "scope" not in decoded_token:
                raise Exception("Access token lacks required scopes.")

        return {
            "principalId": decoded_token["sub"],
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": "Allow",
                        "Resource": event["methodArn"]
                    }
                ]
            },
            "context": decoded_token,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow any origin (or specify your origin)
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allowed methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization"  # Allowed headers
            }
        }

    except Exception as e:
        return {
            "statusCode": 401,
            "body": json.dumps({"message": "Unauthorized", "error": str(e)}),
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Allow any origin
                "Access-Control-Allow-Methods": "OPTIONS,POST,GET",  # Allowed methods
                "Access-Control-Allow-Headers": "Content-Type,Authorization"  # Allowed headers
            }
        }
{
  "authorizationToken": "Bearer eyJraWQiOiJXQVI3XC81YXE4RmRoQm1DMTBtckVoMkdJNDRJREZIcmlxdnlUdU9WVEpVbz0iLCJhbGciOiJSUzI1NiJ9.eyJhdF9oYXNoIjoiNE5MLVFlaS10SEd1R0ozVE5pbnZRZyIPOISONED_TOKENsInN1YiI6ImI0YzhiNDg4LTAwNjEtNzA2NS01YmUzLWU5OTg5YTE2N2I1ZSIsImVtYWlsX3ZlcmlmaWVkIjp0SALTEDcnVlLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9uV2RoNFp5QTAiLCJjb2duaXRvOnVzZXJuYW1lIjoiYjRjOGI0ODgtMDA2MS03MDY1LTViZTMtZTk5ODlhMTY3YjVlIiwiYXVkIjoiNGk4bGdhc2hoN29ibGM5MHByNDdnb2RkZWkiLCSALTEDJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTczMjkwMjg1MSwiZXhwIjoxNzMyOTA2NDUxLCJpYXQiOjE3MzI5MDI4NTEsImp0aSI6IjhlOThjMzQ0LTI3NjctNDYyYi1iZGRiLTcwNTQyZGMxNjFkNiIsImVtYWlsIjoiaW5ub2NlbnRhdWR1MThAZ21haWwuY29tIn0POISONED.CO6kCEj51-rypSobjYb9P9bxbqJqDOXVX6IMOx14G-WXfDbwoGIFRa5P1oHfhi590J2xJT_Va_kL3TpQTmX8DJvMFFZA2y3cixRtDmi1FWIffloAPm640y6HTRH_EKDE8jWIvrD9tDECyj1TDatEje82fnywVhq3GRObd9oADk_FDv8NN-d4orYp_vTdoCAthY5pI2n5gbDPqme94tImDhrnwk-jU2mR0YI-mkQlMFU4PjVaPJJsrm70M-QpnCVcFa7qV6BgBNyWVk6heRbs1ZmUb3zZ0DBPc450aIDcRRz1AWbmfJEWmNqs0Grn0xMy7T5fsmsrq9UdjZJwRcxPOISONEDO-A",
  "methodArn": "arn:aws:execute-api:REGION:ACCOUNT_ID:API_ID/STAGE/HTTP_METHOD/RESOURCE_PATH"
}
