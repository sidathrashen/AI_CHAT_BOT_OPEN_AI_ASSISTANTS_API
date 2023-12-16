import os
import core_functions
import json
import config

# Function to either create a new assistant or load an existing one
def create_assistant(client, tool_data):
    assistant_file_path = 'assistant.json'  # Define the file path for the assistant's configuration

    # Check if the assistant configuration file already exists
    if os.path.exists(assistant_file_path):
        # Open and read the existing assistant configuration file
        with open(assistant_file_path, 'r') as file:
            assistant_data = json.load(file)  # Load the assistant data from the file
            assistant_id = assistant_data['assistant_id']  # Extract the assistant ID
            print("Loaded existing assistant ID.")  # Log that the existing assistant was loaded
    else:
        # No existing assistant found, proceed to create a new one

        # Retrieve the IDs of resource files using a function defined in 'core_functions'
        file_ids = core_functions.get_resource_file_ids(client)

        # Create a new assistant using the OpenAI client
        assistant = client.beta.assistants.create(
            instructions=config.assistant_instructions,  # Set up instructions from the config file
            model="gpt-4-1106-preview",  # Specify the model to be used for the assistant
            tools=[{"type": "retrieval"}] + tool_data["tool_configs"],  # Configure tools for the assistant
            file_ids=file_ids  # Attach resource files identified earlier
        )

        # Log the newly created assistant's ID
        print(f"Assistant ID: {assistant.id}")

        # Save the new assistant's ID in a configuration file for future reference
        with open(assistant_file_path, 'w') as file:
            json.dump({'assistant_id': assistant.id}, file)  # Write the assistant ID to the file
            print("Created a new assistant and saved the ID.")  # Log that a new assistant was created and saved

        assistant_id = assistant.id  # Set the assistant ID for return

    return assistant_id  # Return the assistant ID
