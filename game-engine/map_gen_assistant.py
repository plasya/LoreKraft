from openai import OpenAI
import os
import json
# from dotenv import load_dotenv

# Load environment variables from .env file
# load_dotenv()

# Load API keys from environment variables
openai_api_key = "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"

# Initialize OpenAI client
client = OpenAI(api_key=openai_api_key)

def generate_dnd_map(theme, checkpoints=10):
    # Define the system instruction and user input in the message format
    messages = [
        {
            "role": "system", 
            "content": """You are a specialized system designed to generate a Dungeons & Dragons (DND) map with a given theme and a specified number of checkpoints. You will follow the detailed instruction below to ensure the map is consistent, engaging, and meets the requirements.

# Task:
Generate a DND map and the story based on the given theme and the number of checkpoints. The map must contain a starting point and an ending point, with at least 4 sequential checkpoints and the rest being either sequential or parallel paths.

# Instructions:
1. The output should always be a dictionary named `dnd_map` where the keys are unique place names, such as "Goblin Fortress" or "Ancient Shrine", and the values are lists of places they lead to.
2. Ensure the following structure:
    - The `Start` point must lead to one or more specific places.
    - The `End` point must be reached at the conclusion and have no parallel paths after it.
3. The "Start" and "End" points must have unique and specific names (e.g., "Village Outskirts" for Start, and "Royal Citadel" for End).
4. All locations must be connected — no disconnected or isolated points.
5. Avoid infinite loops or circular paths unless it serves a specific purpose, and ensure they eventually lead to the `End`.
6. There must be at least 4 levels of sequential paths. Each level can contain branching paths, but the path should still eventually lead to the `End`.
7. The names of places (e.g., "Goblin Fortress", "Dragon"s Lair", "Ancient Shrine") should be randomly generated, ensuring variety in each map.
8. Each node that leads to an empty list should represent a dead end in the game.

""" }, 
        { "role": "user", "content": f"""The theme is {theme} and the checkpoints is {checkpoints}.
"""     } 
    ]
    
    # Call GPT-4O to generate the map
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1000,
        temperature=0.7
    )

    # Extract the generated map from the assistant"s response
    dnd_map_code = completion.choices[0].message.content.strip()

    # Safely extract the dictionary portion
    try:
        start = dnd_map_code.find("{")  # Find the start of the dictionary
        end = dnd_map_code.rfind("}") + 1  # Find the end of the dictionary
        map_code_str = dnd_map_code[start:end]  # Extract just the dictionary string
        dnd_map = eval(map_code_str)  # Evaluate the string safely to get the Python dictionary
    except Exception as e:
        print(f"Error while parsing map: {e}, {map_code_str}")
        return None,None

    # Convert dnd_map to JSON string to pass in the next message
    dnd_map_json = json.dumps(dnd_map)

    # Now ask for the start and end points, without appending any additional messages
    messages = [ 
        { "role": "user", 
          "content": f"Given the dictionary: {dnd_map_json}, output ONLY the starting point and end point as start: starting point, end: ending point as a dictionary and NOTHING else" }
    ]

    # Call GPT-4O again to extract start and end points
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,  # Pass the full conversation
        max_tokens=1000,
        temperature=0.7
    )

    start_end = completion.choices[0].message.content.strip()

    # Safely extract the dictionary portion for start and end points
    try:
        start = start_end.find("{")  # Find the start of the dictionary
        end = start_end.rfind("}") + 1  # Find the end of the dictionary
        map_code_str = start_end[start:end]  # Extract just the dictionary string
        start_end_dict = eval(map_code_str)  # Evaluate the string safely to get the Python dictionary
    except Exception as e:
        print(f"Error while parsing start/end points: {e}")
        return dnd_map, [dnd_map.keys()[0], dnd_map.keys()[-1]]

    # print("Start and End Points:", start_end_dict)
    return dnd_map, start_end_dict


def main(): 
    theme = "Avengers save the world from Thanos" 
    checkpoints = 10
    # Generate the DND map and get start/end points
    dnd_map, start_end_dict = generate_dnd_map(theme, checkpoints)

    # Print the generated map and start/end points
    if dnd_map:
        print("Generated DND Map:", dnd_map)
    if start_end_dict:
        print("Start and End Points:", start_end_dict)


if __name__ == "__main__":
    main()
