from dotenv import dotenv_values
from google import genai

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
        contents=f'Explain why does {player_item} {relationship} {current_item}? Keep it short and concise.',
    )
    return response.text