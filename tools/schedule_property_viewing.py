import os
import requests
import re
from datetime import datetime

# Set the webhook URL as an environment variable for security and flexibility
WEBHOOK_URL = "YOUR_WEBHOOK_URL"  # Replace with your actual webhook URL

# Define the tool's configuration for scheduling property viewings
tool_config = {
    "type": "function",
    "function": {
        "name": "schedule_property_viewing",
        "description": "Schedules a property viewing appointment for users.",
        "parameters": {
            "type": "object",
            "properties": {
                "full_name": {
                    "type": "string",
                    "description": "The full name of the user requesting the viewing."
                },
                "email": {
                    "type": "string",
                    "description": "The email address of the user for communication."
                },
                "property_id": {
                    "type": "string",
                    "description": "The unique identifier of the property to be viewed."
                },
                "date_time": {
                    "type": "string",
                    "description": "The preferred date and time for the viewing in YYYY-MM-DD HH:MM format."
                }
            },
            "required": ["full_name", "email", "property_id", "date_time"]  # List of required fields
        }
    }
}

# Function to schedule a property viewing
def schedule_property_viewing(arguments):
    """
    This function schedules a property viewing based on user-provided details and sends the data to a configured webhook.

    :param arguments: dict, contains details for scheduling the viewing including full_name, email, property_id, and date_time.
    :return: dict or str, the response from the webhook or an error message in case of failure.
    """
    # Extracting individual details from the arguments
    full_name = arguments.get('full_name')
    email = arguments.get('email')
    property_id = arguments.get('property_id')
    date_time = arguments.get('date_time')

    # Check if the email is in a valid format using regex
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format. Please provide a valid email address."

    # Validate the date and time format to ensure it follows the specified structure
    try:
        datetime.strptime(date_time, '%Y-%m-%d %H:%M')
    except ValueError:
        return "Invalid date and time format. Please use YYYY-MM-DD HH:MM."

    # Organize the data into a format suitable for sending to the webhook
    data = {
        "full_name": full_name,
        "email": email,
        "property_id": property_id,
        "date_time": date_time
    }

    # Attempt to send the data to the webhook and handle any potential errors
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        # Check for successful response codes
        if response.status_code in [200, 201]:
            return "Property viewing scheduled successfully."
        else:
            # Return an error message if the response code indicates a failure
            return f"Error scheduling property viewing: {response.text}"
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request, such as network issues
        return f"Failed to send data to the webhook: {e}"
