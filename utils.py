from dotenv import dotenv_values
from google import genai
import emoji
import difflib

config = dotenv_values(".env")

def get_relationship(client, current_item: str, player_item: str) -> str:
    """
    :param current_item: current item to beat
    :param player_item: proposed item by player
    :return: the string "Win" or "Lose"
    """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f'Does {player_item} beat or not beat {current_item}?',
        config={
            'response_mime_type': 'text/x.enum',
            'response_schema': {
                "type": "STRING",
                "enum": ["beat", "not beat"],
            },
        },
    )
    return response.text

def get_explanation(client, current_item: str, player_item: str, relationship: str) -> str:
    """
    :param current_item: current item to beat
    :param player_item: proposed item by player
    :param relationship: the string "Win" or "Lose"
    :return: short explanation
    """
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=f'Create a plausible explanation on why does {player_item} {relationship} {current_item}? Assume that it is always true. Keep it short and concise.',
    )
    return response.text

def find_closest_emoji(word):
    all_emojis = emoji.EMOJI_DATA  # Dictionary with emoji metadata
    emoji_descriptions = {e: data['en'] for e, data in all_emojis.items() if 'en' in data}

    # Find the closest match among emoji descriptions
    best_match = None
    highest_ratio = 0

    for emj, desc in emoji_descriptions.items():
        ratio = difflib.SequenceMatcher(None, word.lower(), desc.lower()).ratio()
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = emj

    return best_match if best_match else ""

def char_is_emoji(char):
    return char in emoji.EMOJI_DATA