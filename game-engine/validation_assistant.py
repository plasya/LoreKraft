from openai import OpenAI
import os
import asyncio
import json
from pymongo import MongoClient  # MongoDB integration
from bson import ObjectId  # To handle ObjectId conversion
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
mongo_uri = os.getenv("MONGO_URI")  # MongoDB connection URI

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

# Connect to MongoDB
mongo_client = MongoClient(mongo_uri)
db = mongo_client['Hackathon']  # Use your actual database name
characters_collection = db['characters']  # Collection for character data

# Function to convert MongoDB ObjectId to string and handle serialization
def serialize_character(character):
    # Convert ObjectId to string and ensure all fields are serializable
    if '_id' in character:
        character['_id'] = str(character['_id'])
    return character

# Function to query MongoDB for character data
def get_character_info(character_name):
    # Query the character based on character_name
    character = characters_collection.find_one({"character_name": character_name})
    print(character)
    if character:
        print(serialize_character(character))
        return str(character)  # Serialize the character for JSON compatibility

    else:
        return "Nothing here"

# Validation Assistant setup with function tool
validation_assistant = client.beta.assistants.create(
    name="Validation Assistant",
    instructions=f"""
Validate player actions based on their character's attributes, abilities, and the game's context.

# Steps

1. **Retrieve Character Information**: Access the MongoDB database using the 'get_character_info' function to obtain the player's character information using their character name.
2. **Action Validation**:
   - Compare the player's attempted action with their character's attributes and abilities.
   - Determine if the action aligns with what the character can perform within the game's context.
3. **Determine Validity**:
   - Conclude whether the action is valid (True) or invalid (False) based on the validation process.
4. **Provide Reasoning**: Clarify the reasons behind the validity decision, ensuring it's comprehensive and related to the character’s attributes.
5. **Suggest Alternatives**: If the action is deemed invalid, offer a feasible and contextually suitable alternative action.

# Output Format

The output should be in JSON format and include the following fields:
- `action`: The action the player attempted.
- `validity`: A boolean value indicating the validity of the action.
- `reason`: A descriptive string explaining why the action is valid or invalid.
- `suggestion`: If the action is invalid, provide a recommended alternative action.

# Example

**Input:**
- Player action: "Fly across the sky"
- Character: "Pureblood"

**Output:(JSON Format)**

  "action": "Fly across the sky",
  "validity": false,
  "reason": "Purebloods cannot fly.",
  "suggestion": "Consider using Noble Strike instead."

# Notes

- Ensure your validation process relies on character attributes retrieved from the MongoDB database.
- Suggestions should be contextually appropriate and provide the player with viable alternative actions.
    """,
    tools=[
        {"type": "function",
         "function": {
            "name": "get_character_info",
            "description": "Get the information of a character by their character name",
            "parameters": {
                "type": "object",
                "properties": {
                    "character_name": {
                        "type": "string",
                        "description": "The name of the character to retrieve info for"
                    }
                },
                "required": ["character_name"]
            }
        }}
    ],
    model="gpt-4o",
)

# Function to handle assistant logic and generate a validation response
async def get_validation_response(character_name, action):
    # Create a new thread for the conversation
    new_thread = client.beta.threads.create()

    # Create a message in the new thread with the content from the player
    client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=f"Character Name: {character_name}, Action: {action}"
    )

    # Execute the assistant run and poll for its status
    run = client.beta.threads.runs.create_and_poll(
        thread_id=new_thread.id,
        assistant_id=validation_assistant.id,
    )

    # If the run is complete, print the messages
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=new_thread.id
        )
        print(messages)

    else:
        print(f"Run is not completed. Current status: {run.status}")

        # Define the list to store tool outputs
        tool_outputs = []

        # Check if there are required tool actions
        if run.required_action and run.required_action.submit_tool_outputs:
            # Loop through each tool call
            for tool in run.required_action.submit_tool_outputs.tool_calls:
                # Extract the arguments for get_character_info from the tool
                tool_arguments = json.loads(tool.function.arguments)
                character_name = tool_arguments.get("character_name")

                # Fetch character info using the tool's input parameters
                character_info = get_character_info(character_name)

                # Add the character info to the tool outputs
                if character_info:
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": character_info
                    })

        # Submit all tool outputs if there are any
        if tool_outputs:
            try:
                # Submit tool outputs and re-poll for the run status
                run = client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=new_thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
                print("Tool outputs submitted successfully.")
            except Exception as e:
                print(f"Failed to submit tool outputs: {e}")
        else:
            print("No tool outputs to submit.")

        # After submitting tool outputs, check the run status again
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=new_thread.id
            )
            # Extract and print the assistant's message
            for message in messages.data:
                if message.role == "assistant":
                    validation_response = message.content[0].text.value
                    print(f"Validation Response:\n{validation_response}")
                    return validation_response
        else:
            print(f"Run is still not completed. Current status: {run.status}")

# Example usage of the validation assistant
async def main():
    character_name = "Pureblood"
    action = "Fly across the sky"

    # Get validation response
    validation_result = await get_validation_response(character_name, action)

    if validation_result:
        print("Validation Result:", validation_result)
    else:
        print("There was an issue retrieving the validation result.")

# Run the asynchronous main function
if __name__ == "__main__":
    asyncio.run(main())
