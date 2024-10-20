from map_outline import m
from pymongo import MongoClient  # MongoDB integration
import os
from dotenv import load_dotenv
import ast
from openai import OpenAI
from validation_assistant import get_validation_response
##test
num_players = 3
player_id = 1
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)


mongo_uri = os.getenv("MONGO_URI")  # MongoDB connection URI
mongo_client = MongoClient(mongo_uri)


#### Meta-data 1: Map information
### Convert map object to JSON for LLM interpretability
def map_to_dict(map_obj):
    map_dict = {}
    for node_name, node_obj in map_obj.test.items():
        map_dict[node_name] = {
            'next_nodes': [n.name for n in node_obj.next_nodes],
            'events': node_obj.events
        }
    return map_dict


### Json for map object
m_json = map_to_dict(m)
### list of visited nodes
visited_node = m.list_visited_nodes()

#### Meta-data 2: Player information
db = mongo_client['Hackathon']  # Use your actual database name
characters_collection = db['players']  # Collection for character data


### Types of events
event_types = {
    'common' : "",
    'friendly': "black market, bazar, sketchy salesperson",
    'delayed': "suddenly appears - trap, horde of low-level enemies"
}


#### Meta-data 3: Retrieve all enemy stats
### Retrieve all information where character_role = Enemy or Enemy Boss - enemy_characters
# Retrieve all documents
db = mongo_client['Hackathon']  # Use your actual database name
characters_collection = db['characters']  # Collection for character data

# Query to only retrieve the character_name, background, and Weapon fields
all_characters = characters_collection.find({}, {'character_name': 1, 'background': 1, 'Weapon': 1})

# List to store matching enemies
enemy_characters = []

# Loop through each document
for character in all_characters:
    try:
        # Convert the string representation of the list into an actual Python list (if needed)
        character_roles = ast.literal_eval(character.get("character_roles", "[]"))

        # Check if "Enemy" or "Enemy Boss" is in the list
        if "Enemy" in character_roles or "Enemy Boss" in character_roles:
            # Add only the relevant fields (character_name, background, Weapon)
            enemy_data = {
                'character_name': character.get('character_name'),
                'background': character.get('background'),
                'Weapon': character.get('Weapon')
            }
            enemy_characters.append(enemy_data)
    except Exception as e:
        print(f"Error processing character {character.get('_id')}: {e}")



dungeon_master = client.beta.assistants.create(
    name="Dungeon Master",
    instructions=f"""
You are a Dungeon Master guiding a player through a story-driven game. The game uses a map where each node represents a location with associated events. Your role is to generate a creative and immersive narrative for the player based on the current node, the event history, and map data provided.

### Types of Events:
Each node has events of the following types:
- **Common**: Regular encounters such as low-level enemy fights, exploration, or environmental interactions.
- **Friendly**: Encounters with traders, bazaars, sketchy salespeople, or black market dealings.
- **Delayed**: Events triggered after a countdown. A delayed event has an associated countdown number that decreases every time the player visits the node. When the countdown reaches 0, the delayed event triggers.
- **Trigger**: These events introduce new elements to an unvisited node, such as spawning a new enemy or trap.

### Your Task:
1. **Narrative Generation**: Based on the current node, combine all possible events (common, friendly, delayed, or trigger) and narrate the story accordingly. Be as creative as possible, grounded in the facts provided.
    - If a delayed event's countdown reaches 0, trigger it in the current node. The countdown is represented in the format: key is delayed and value is 'event_cAS7': 2, where 2 is the countdown.
    - You can dynamically add new events or escalate existing events based on the story's progression.
2. **Node Management**: After the narrative, determine the next node the player will move to based on the current node's `next_nodes` list. If there are multiple options, choose based on the story's context or player's previous choices.
3. **Decision Making**: Provide the player with two suggestions for what actions they can take next.
4. **Image Generation Prompt**: After generating the narrative, create a prompt to generate 3 image frames that visually represent key moments in the narrative.
5. **Player Turn**: Maintain a circular queue for the players according to the given number of players. Switch the player number making sure everyone gets one turn and the cycle repeats

### Example Map Data (JSON format):
The map is represented as a dictionary where:
- Each key is a location (node).
- `next_nodes` lists the next possible locations the player can go to after completing the current event.
- `events` contains the types of events (common, friendly, delayed, trigger) that can occur in the node.

Here is the map:
{m_json}  # The serialized map object from your game will go here.

### Enemy Data:
For any combat or enemy encounters, you can use the following characters from the `enemy_characters` collection. Each character has stats, abilities, and a description, for example:
{enemy_characters}  # Provide a list of enemy characters for potential combat encounters.

# Visited node: 
{visited_node} #List of all past visited nodes

# Number of players:
{num_players} 

Example Input:
  "player_id": "1",
  "character_name": "Pureblood"
  "action": "Fly across the sky",
  "validity": false,
  "reason": "Purebloods cannot fly.",
  "suggestion": "Consider using Noble Strike instead."

# Output Format

The output should be a JSON object that contains:
1. **Narrative**: The creative story based on the current node's events.
2. **Current Node**: The name of the node the player is currently in after the narrative. use the map to pick a suitable next node
3. **Next Moves**: Two suggestions for the player's next actions.
4. **Image Prompt**: A prompt for generating 3 image frames that visually represent key moments in the narrative.

### Example Output (json)

    "narrative": "Unfornuately while trying to fly, you fell into the city of Wakanda where the towering vibranium mines loom ahead. Suddenly, you hear the clashing of weapons—a group of Goblins  ambushes you. Their leader shouts, 'Take them down!' You must decide whether to fight or flee.",
    "current_node": "Wakanda",
    "next_moves": ["Fight the Hydra agents", "Attempt to flee and reach the Quantum Tunnel"],
    "image_prompt": "Generate 3 image frames: 1. The player entering Wakanda with the vibranium mines in the background. 2. The Hydra agents ambushing the player. 3. A close-up of the Hydra leader issuing a command to attack."
    "player_turn" : 2 

The complexity of the next_moves and narration should depend on the history and other meta-data provided. You must adhere to the structure and include all components in the output. Be as creative as possible with the narrative while ensuring consistency with the map, events, and enemy data provided.
    """,
    model="gpt-4o",
)

# Function to handle assistant logic and generate a validation response
def get_dungeon_master_response(player_id, action):
    # Create a new thread for the conversation
    new_thread = client.beta.threads.create()

    validation_result = get_validation_response("Barbarian", "I'm player 1 and I'd like to start the match")
    # Create a message in the new thread with the content from the player
    client.beta.threads.messages.create(
        thread_id=new_thread.id,
        role="user",
        content=f"{validation_result}"
    )

    # Execute the assistant run and poll for its status
    run = client.beta.threads.runs.create_and_poll(
        thread_id=new_thread.id,
        assistant_id=dungeon_master.id,
    )

    # After submitting tool outputs, check the run status again
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id=new_thread.id
        )
        # Extract and print the assistant's message
        for message in messages.data:
            if message.role == "assistant":
                dg_response = message.content[0].text.value
                return dg_response
    else:
        print(f"Run is still not completed. Current status: {run.status}")
        return None


def main():
    player_action = "I'm player 1 and I'd like to start the match"
    player_id = 1
    
    # Get Dungeon Master response
    response = get_dungeon_master_response(player_id, player_action)
    
    # Process response and display output
    if response:
        print(f"Dungeon Master Response: {response}")

    else:
        print("There was an issue generating the Dungeon Master response.")

# Run the main function
if __name__ == "__main__":
    main()

