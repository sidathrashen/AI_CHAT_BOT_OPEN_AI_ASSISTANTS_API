import os
import logging
from flask import Flask, request, jsonify
import openai
import core_functions
import assistant

# Configure the logging level to INFO for better visibility of operations
logging.basicConfig(level=logging.INFO)

# Check if the OpenAI library's version is compatible with the requirements
core_functions.check_openai_version()

# Initialize a Flask application for handling web requests
app = Flask(__name__)

# Retrieve the OpenAI API key from environment variables and validate its presence
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("No OpenAI API key found in environment variables")
# Initialize the OpenAI client with the retrieved API key
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Load tool configurations and function mappings from the 'tools' directory
tool_data = core_functions.load_tools_from_directory('tools')

# Create a new assistant or load an existing one based on the configuration
assistant_id = assistant.create_assistant(client, tool_data)

# Define a route to initiate a conversation with the assistant
@app.route('/start', methods=['GET'])
def start_conversation():
    # Verify the API key to ensure authorized access
    core_functions.check_api_key()
    logging.info("Starting a new conversation...")
    # Create a new thread for the conversation
    thread = client.beta.threads.create()
    logging.info(f"New thread created with ID: {thread.id}")
    # Return the thread ID as a response
    return jsonify({"thread_id": thread.id})

# Define a route for chatting with the assistant
@app.route('/chat', methods=['POST'])
def chat():
    # Verify the API key for security
    core_functions.check_api_key()
    # Extract data from the POST request
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    # Check if thread_id is provided in the request
    if not thread_id:
        logging.error("Error: Missing thread_id")
        return jsonify({"error": "Missing thread_id"}), 400

    # Log the received user message and the corresponding thread ID
    logging.info(f"Received message: {user_input} for thread ID: {thread_id}")
    # Send the user's message to the OpenAI thread
    client.beta.threads.messages.create(thread_id=thread_id,
                                        role="user",
                                        content=user_input)
    # Create a run to get the assistant's response
    run = client.beta.threads.runs.create(thread_id=thread_id,
                                          assistant_id=assistant_id)
    # Process any tool calls that are required by the assistant's response
    core_functions.process_tool_calls(client, thread_id, run.id, tool_data)

    # Retrieve the assistant's response messages
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value
    # Log the assistant's response
    logging.info(f"Assistant response: {response}")
    # Return the assistant's response as a JSON object
    return jsonify({"response": response})

# Run the Flask app when the script is executed directly
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
