import utils
from google import genai
from dotenv import dotenv_values
config = dotenv_values(".env")

class Game:
    def __init__(self):
        """
        Main instance of a game. Assume that every time the game starts you call this object.
        """
        self.is_alive = True
        self.current_object = "Rock"
        self.has_been_played = set()
        # instantiate the client
        self.client = genai.Client(api_key=config["GEMINI_API_KEY"])
        self.score = 0
        # main game logic
        while self.is_alive:
            print(f"What beats {self.current_object}?")
            print(f"Current score: {self.score}")
            player_choice = input("Input: ")

            if player_choice.lower() in self.has_been_played:
                print("This has been already played! Try being more original 😀")
                continue

            # Determine the relationship between player choice using a LLM wrapper
            relationship = utils.get_relationship(self.client, self.current_object, player_choice)
            explanation = utils.get_explanation(self.client, self.current_object, player_choice, relationship)

            if relationship == 'not beat':
                print(f"{player_choice.title()} does not beat {self.current_object.title()}. {explanation}")
                print(f"Final score: {self.score}")
                break

            # at this point the player could only win
            print(f"{player_choice.title()} beats {self.current_object.title()}. {explanation}")
            self.score += 1
            self.has_been_played.add(player_choice.lower())
            self.current_object = player_choice