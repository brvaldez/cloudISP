import azure.functions as func
import logging
from azure.cosmos import CosmosClient, exceptions
import os

COSMOS_CONNECTION_STRING = os.getenv("COSMOS_CONNECTION_STRING")
DATABASE_NAME = "CounterData"                       # Replace with your database name
CONTAINER_NAME = "ResumeCounter"                     # Replace with your container name
ITEM_ID = "1"                                    # Unique ID for the counter document 

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)
def update_view_count():
    try:
        # Initialize Cosmos DB client using the connection string
        client = CosmosClient.from_connection_string(COSMOS_CONNECTION_STRING)
        database = client.get_database_client(DATABASE_NAME)
        container = database.get_container_client(CONTAINER_NAME)

        # Attempt to read the document
        item = container.read_item(item=ITEM_ID)

        # Increment the view count
        item["count"] += 1

        # Update the document in the database
        container.replace_item(item=ITEM_ID, body=item)

        print(f"View count updated to {item['count']}.")

    except exceptions.CosmosResourceNotFoundError:
        # If the document does not exist, create it
        print("Document not found. Creating a new one.")
        item = {
            "id": ITEM_ID,
            "count": 1
        }
        container.create_item(body=item)
        print(f"View count initialized to {item['views']}.")

    except Exception as e:
        print(f"An error occurred: {e}")

@app.route(route="counter_trigger")
def counter_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("HTTP trigger function processed a request.")

    try:
        # Update the view count
        update_view_count()
        return func.HttpResponse(
            "View count updated successfully.",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Failed to update view count: {e}")
        return func.HttpResponse(
            "Failed to update view count.",
            status_code=500
        )

@app.route(route="http_trigger", auth_level=func.AuthLevel.FUNCTION)
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )