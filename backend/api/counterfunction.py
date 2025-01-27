import logging
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import os

# Cosmos DB configuration
COSMOS_DB_CONNECTION_STRING = os.getenv("COSMOS_DB_CONNECTION_STRING")
DATABASE_NAME = "CounterData"
CONTAINER_NAME = "ResumeCounter"

# Initialize Cosmos DB client
client = CosmosClient.from_connection_string(COSMOS_DB_CONNECTION_STRING)
database = client.get_database_client(DATABASE_NAME)
container = database.get_container_client(CONTAINER_NAME)

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Retrieve the current view count
        try:
            item = container.read_item(item="1")
            view_count = item["count"]
        except exceptions.CosmosResourceNotFoundError:
            # Initialize the count if the document doesn't exist
            view_count = 0
            container.create_item({
                "id": "viewCount",
                "count": view_count
            })

        # Increment the view count
        view_count += 1

        # Update the view count in Cosmos DB
        container.upsert_item({
            "id": "1",
            "count": view_count
        })

        # Return the updated view count
        return func.HttpResponse(
            json.dumps({"viewCount": view_count}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error updating view count: {str(e)}")
        return func.HttpResponse(
            "An error occurred while updating the view count.",
            status_code=500
        )
