import azure.functions as func
import logging
import json
from azure.cosmos import CosmosClient, exceptions


app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Initialize the Cosmos client and container
cosmos_client = CosmosClient("https://bruno-ispdata.documents.azure.com:443/", "Q5tIDXHfEHUxV6xxSy6v7GJrsE7OSKt5QTxxiTW4ywetb161zzfxHcWowmoWoEa0Wx8jWGVB9UQQACDbeEocKw==")
database = cosmos_client.get_database_client("ResourceCounter")
container = database.get_container_client("CounterData")

@app.route(route="update_counter", methods=["GET"])
def update_counter(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # ID of the counter document
        counter_doc_id = "1"

        # Fetch the current counter document
        counter_doc = container.read_item(item=counter_doc_id, partition_key=counter_doc_id)
        current_count = counter_doc["count"]

        # Increment the counter
        updated_count = current_count + 1
        counter_doc["count"] = updated_count

        # Update the counter document in the database
        container.replace_item(item=counter_doc_id, body=counter_doc)

        # Return the updated count as a JSON response
        return func.HttpResponse(
            json.dumps({"count": updated_count}),
            mimetype="application/json",
            status_code=200
        )
    except exceptions.CosmosResourceNotFoundError:
        # Create the counter document if it doesn't exist
        initial_count = {"id": "1", "count": 1}
        container.create_item(body=initial_count)
        return func.HttpResponse(
            json.dumps({"count": 1}),
            mimetype="application/json",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error updating counter: {e}")
        return func.HttpResponse("Error updating counter.", status_code=500)
