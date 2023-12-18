import json
import importlib.util
from flask import request, abort
import time
import logging
import openai
import os
from packaging import version

# Retrieve custom API key from environment variables
CUSTOM_API_KEY = os.environ.get('CUSTOM_API_KEY')

# Function to verify the API key in the request header
def check_api_key():
    # Get the API key from the request header
    api_key = request.headers.get('X-API-KEY')
    # Abort with a 401 Unauthorized status if the API key doesn't match
    if api_key != CUSTOM_API_KEY:
        abort(401)

# Function to ensure the OpenAI library version meets requirements
def check_openai_version():
    # Define the minimum required version
    required_version = version.parse("1.1.1")
    # Parse the current version of OpenAI library
    current_version = version.parse(openai.__version__)
    # Raise an error if the current version is less than required
    if current_version < required_version:
        raise ValueError(
            f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1"
        )
    else:
        # Log a message if the version is compatible
        logging.info("OpenAI version is compatible.")

# Function to process tool calls initiated by the assistant's API
def process_tool_calls(client, thread_id, run_id, tool_data):
    while True:
        # Retrieve the status of the current run
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run_status.status == 'completed':
            print(f"run_status for thread_id: {thread_id} is {run_status}")
            break
        elif run_status.status == 'requires_action':
            print(f"run_status for thread_id: {thread_id} is {run_status}")

            # Process each tool call that requires action
            for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name

                try:
                    # Decode the JSON arguments for the tool call
                    arguments = json.loads(tool_call.function.arguments)
                except json.JSONDecodeError as e:
                    # Log an error if JSON decoding fails
                    logging.error(f"JSON decoding failed: {e.msg}. Input: {tool_call.function.arguments}")
                    arguments = {}  # Set default value for arguments

                # Execute the corresponding function if it exists in the tool data
                if function_name in tool_data["function_map"]:
                    function_to_call = tool_data["function_map"][function_name]
                    output = function_to_call(arguments)
                    # Submit the output of the tool call
                    client.beta.threads.runs.submit_tool_outputs(
                        thread_id=thread_id,
                        run_id=run_id,
                        tool_outputs=[{
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(output)
                        }]
                    )
                else:
                    # Log a warning if the function is not found in tool data
                    logging.warning(f"Function {function_name} not found in tool data.")
            time.sleep(1)  # Sleep for a short period before the next iteration

# Function to retrieve IDs of all available resource files
def get_resource_file_ids(client):
    file_ids = []
    resources_folder = 'resources'
    # Check if the resources folder exists
    if os.path.exists(resources_folder):
        # Iterate over files in the resources folder
        for filename in os.listdir(resources_folder):
            file_path = os.path.join(resources_folder, filename)
            if os.path.isfile(file_path):
                with open(file_path, 'rb') as file:
                    # Create a file in the OpenAI client and append its ID to the list
                    response = client.files.create(file=file, purpose='assistants')
                    file_ids.append(response.id)
    return file_ids

# Function to load tools from a specified directory
def load_tools_from_directory(directory):
    tool_data = {"tool_configs": [], "function_map": {}}

    # Iterate over Python files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            module_path = os.path.join(directory, filename)
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # Load tool configuration if present
            if hasattr(module, 'tool_config'):
                tool_data["tool_configs"].append(module.tool_config)

            # Map callable functions from the module to their names
            for attr in dir(module):
                attribute = getattr(module, attr)
                if callable(attribute) and not attr.startswith("__"):
                    tool_data["function_map"][attr] = attribute

    return tool_data
