import os
import requests

# Retrieve the RAPID API key from environment variables
RAPID_API_KEY = os.environ['RAPID_API_KEY']

# Configuration for the 'search_real_estate_listings' tool
tool_config = {
    "type": "function",
    "function": {
        "name": "search_real_estate_listings",
        "description": "Search for real estate listings based on various parameters.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Location to search (city, zip code, or address)."
                },
                "offset": {
                    "type": "number",
                    "description": "Offset results from the start, default is 0."
                },
                "limit": {
                    "type": "number",
                    "description": "Maximum number of results to return, default is 50."
                },
                # Additional optional parameters can be included here
            },
            "required": ["location"]  # 'location' is a mandatory parameter
        }
    }
}

# Function to search real estate listings using the Rapid API
def search_real_estate_listings(arguments):
    """
    Searches for real estate listings using the specified parameters via the Rapid API.

    :param arguments: dict, contains search parameters such as location, offset, and limit.
    :return: dict or str, the response from the API in JSON format or an error message.
    """
    # Define the API endpoint and headers for the request
    url = "https://us-real-estate-listings.p.rapidapi.com/for-sale"
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,  # API key for authentication
        "X-RapidAPI-Host": "us-real-estate-listings.p.rapidapi.com"
    }

    # Prepare query parameters from the arguments provided
    query_params = {
        key: arguments.get(key)
        for key in arguments if arguments.get(key) is not None
    }

    # Attempt to make the API request
    try:
        response = requests.get(url, headers=headers, params=query_params)
        response.raise_for_status()  # Raise an exception for HTTP error responses
        return response.json()  # Return the response in JSON format
    except requests.exceptions.RequestException as e:
        # Return an error message in case of request failure
        return f"Error: {str(e)}"
