import azure.functions as func
import logging
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Path to the HTML file
    html_file_path = os.path.join(os.path.dirname(__file__), 'brunoresume.html')

    try:
        # Read the HTML file
        with open(html_file_path, 'r') as file:
            html_content = file.read()
        
        # Return the HTML content as the response
        return func.HttpResponse(html_content, mimetype='text/html', status_code=200)
    except Exception as e:
        logging.error(f"Error reading HTML file: {e}")
        return func.HttpResponse("Error reading HTML file.", status_code=500)