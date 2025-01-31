"""
Author: Tam Hoang, hoang49@purdue.edu
Assignment: 12.2.1 - Final Project
Date: 12/02/2024

Description:
    Create the game “Code Breakers”, which is a guessing game based on the game Mastermind created in the 1970s. 
    In this game, a random code will be generated by the computer which is between and characters long and only contains the digits through (inclusive). 

Contributors:
    Name, login@purdue.edu [repeat for each]

My contributor(s) helped me:
    [ ] understand the assignment expectations without
        telling me how they will approach it.
    [ ] understand different ways to think about a solution
        without helping me plan my solution.
    [ ] think through the meaning of a specific error or
        bug present in my code without looking at my code.
    Note that if you helped somebody else with their code, you
    have to list that person as a contributor.

Academic Integrity Statement:
    I have not used source code obtained from any unauthorized
    source, either modified or unmodified; nor have I provided
    another student access to my code.  The project I am
    submitting is my own original work.
"""

"""Import additional modules below this line (starting with unit 6)."""
import random
import datetime
import json
import os

"""Write new functions below this line (starting with unit 4)."""

save_file = 'save_files.json'

#______________________________________________display

def validate_guess(guess):
    if len(guess) not in [4, 5, 6]:
        return f"Guess length must be between 4 and 6. You entered: {len(guess)}"
    if not all(c in '012345' for c in guess):
        return "Guess must be only numbers 0 through 5."
    return "valid"

def generate_solution(min_length, max_length):
    length = random.randint(min_length, max_length)
    return ''.join(str(random.randint(0, 5)) for _ in range(length))

def evaluate_guess(solution, guess):
    reds = sum(1 for i, j in zip(solution, guess) if i == j)
    whites = sum(min(guess.count(n), solution.count(n)) for n in set(guess)) - reds
    return reds, whites

def display_board(solution, guesses, reds, whites, solution_revealed):
    # Display the top of the board with the solution
    solution_display = solution if solution_revealed else ['o'] * 6
    print("   ==================+=====")
    if solution_revealed:
        print("    " + "  ".join(solution_display) + "  o" * (6 - len(solution))+ " | R W  ")
    else:
        print("    " + "  ".join(solution_display) + " | R W  ")

    print("   ==================+=====")

    # Display empty rows if there are fewer guesses than the max allowed
    for _ in range(10 - len(guesses)):
        print("    o  o  o  o  o  o | 0 0  ")

    # Display the guesses and the pins
    for guess, red, white in zip(reversed(guesses), reversed(reds), reversed(whites)):
        # Pad the guess if it's shorter than 6 characters
        padded_guess = (guess + ['o'] * (6 - len(guess)))[:6]
        print("    " + "  ".join(padded_guess) + f" | {red} {white}  ")

    print("   ==================+=====")

#_______________________________________________________________________save games
    
def display_save_slots():
    slots = get_save_slots()

    print("\nFiles:")
    print("--------------------------------------------------------------------------")
    for slot, data in slots.items():
        if data is None or 'name' not in data:
            print(f"   {slot}: empty")
        else:
            saved_time = data['timestamp']
            print(f"   {slot}: {data['name']} - Time: {saved_time}")

def save_game(slot, game_state):
    slots = get_save_slots()
    player_name = get_player_name()  # Function to get the player's name, ensuring it has no special characters
    game_state['name'] = player_name  # Add the player's name to the game state
    game_state['timestamp'] = datetime.datetime.now().isoformat(timespec="seconds")

    slots[slot] = game_state

    with open(save_file, 'w') as f:
        json.dump(slots, f, indent=4)
    
    print(f"Game saved in slot {slot} as {player_name}.")

def load_game():
    display_save_slots()
    slots = get_save_slots()
    while True:
        slot = input("What save would you like to load (1, 2, 3, or c to cancel): ")
        if slot in ['1','2','3']:
            if slot in slots and slots[slot] is not None:
                print("\nResume Game:")
                print("--------------------------------------------------------------------------")
                game_state = slots[slot]
                break
            else:
                print("That file is empty!")
        elif slot == 'c':
            print("cancelled\n")
            game_state = None
            break
        else:
            print("That is an invalid selection.")
    return game_state
       

def is_valid_name(name):
    return all(char.isalnum() or char.isspace() for char in name)

def get_player_name():
    while True:
        name = input("What is your name (no special characters): ")
        if is_valid_name(name):
            return name
        else:
            print("That is an invalid name.")

def get_save_slots():
    try:
        with open(save_file, 'r') as f:
            content = f.read().strip()
            # If the file is empty, set slots to an empty dictionary
            if not content.strip():
                slots = {"1": None, "2": None, "3": None}
            else:
                slots = json.loads(content)

    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or JSON is invalid, initialize with empty slots
        slots = {"1": None, "2": None, "3": None}
    return slots

#____________________________________rules

def display_header():
    print("You are a member of the Unladened Swallow Society, tasked with cracking")
    print("the notorious Holy Grail lock. This lock secures a vault containing all")
    print("the EBEC grades, locked away by IU. To retrieve your grades, you'll need")
    print("to break through this lock. Fortunately, the creators at IU made an error")
    print("when building it, so the lock will provide hints about the code. However,")
    print("you don't know the passcode length and only have 10 guesses. Use them")
    print("wisely--if you fail, you could be turned into a newt, the grades might be")
    print("destroyed, or, even worse, you might have to rewrite the time calculator!\n")
    print("Will you be able to break this lock before your grades are lost forever?\n")


def display_rules():
    print("\nRules:")
    print("--------------------------------------------------------------------------")
    print("1. You get 10 guesses to break the lock.\n")
    print("2. Guess the correct code to win the game.\n")
    print("3. Codes can be either 4, 5, or 6 digits in length.\n")
    print("4. Codes can only contain digits 0, 1, 2, 3, 4, and 5.\n")
    print("5. Clues for each guess are given by a number of red and white pins.\n")
    print("   a. The number of red pins in the R column indicates the number of digits")
    print("      in the correct location.")
    print("   b. The number of white pins in the W column indicates the number of")
    print("      digits in the code, but in the wrong location.")
    print("   c. Each digit of the solution code or guess is only counted once in the")
    print("      red or white pins.\n")

def main_menu():
    print("Menu:")
    print("--------------------------------------------------------------------------")
    print("   1: Rules")
    print("   2: New Game")
    print("   3: Load Game")
    print("   4: Quit")
    choice = input("Choice: ")
    return choice

def start_game(game_state):
    solution = game_state['solution']
    guesses = game_state['guesses']
    red_pins = game_state['reds']
    white_pins = game_state['whites']
    num_guess = game_state['num_guess']

    display_board(solution, guesses, red_pins, white_pins, False)

    while num_guess < 10:
        guess = input("What is your guess (q to quit, s to save and quit): ")
        if guess.lower() == 'q':
            print("Ending Game.\n")
            break
        elif guess == 's':
            display_save_slots()
            while True:
                slot = input("What save would you like to overwrite (1, 2, 3, or c to cancel): ")
                if slot in ['1', '2', '3']:
                    game_state = {'solution': solution, 'guesses': guesses, 'reds': red_pins, 'whites': white_pins, 'num_guess': num_guess}
                    save_game(slot, game_state)
                    print("Ending Game.\n")
                    break
                elif slot.lower() == 'c':
                    print("cancelled")
                    display_board(solution, guesses, red_pins, white_pins, False)
                    break
                else:
                    print("That is an invalid selection.")
            if not slot.lower() == 'c':
                break
        
        elif len(guess) in [4, 5, 6] and all(char in "012345" for char in guess):
            guess_list = list(guess)
            red, white = evaluate_guess(solution, guess_list)
            guesses.append(guess_list)
            red_pins.append(red)
            white_pins.append(white)
            num_guess += 1
            if guess == solution:
                display_board(solution, guesses, red_pins, white_pins, True)
                print("Congratulations, you broke the lock!\nThe grades are safe!\n")
                break
            else:
                if num_guess < 10:
                   display_board(solution, guesses, red_pins, white_pins, False)
        else:
            if not guess.isdigit() and guess != "":
                print(f'Your guess was "{guess}". It must be only numbers!')
            elif any(char not in "012345" for char in guess):
                print(f'Your guess was "{guess}". It must be only numbers 0 through 5.')
            elif len(guess) < 4:
                print(f'Your guess was "{guess}". This is too short.')
                print("Guess lengths must be between 4 and 6.")
            elif len(guess) > 6:
                print(f'Your guess was "{guess}". This is too long.')
                print("Guess lengths must be between 4 and 6.")

    else:
        display_board(solution, guesses, red_pins, white_pins, True)
        print("You hear a machine yell OUT OF TRIES!")
        print("  ...")
        print("Is that burning you smell?")
        print("  ...")
        print("OH, NO! It looks like IU has destroyed all the EBEC grades!\n\n")

def main():
    display_header()
    while True:
        choice = main_menu()
        if choice == '1':
            display_rules()
        elif choice == '2':
            print("\nNew Game:")
            print("--------------------------------------------------------------------------")
            game_state = {
                'solution': generate_solution(4, 6),
                'guesses': [],
                'reds': [],
                'whites': [],
                'timestamp': None,
                'name': None,
                'num_guess': 0
            }
            start_game(game_state)
        elif choice == '3':
            game_state = load_game()
            if game_state is not None:
                start_game(game_state)
            
        elif choice == '4':
            print("Goodbye")
            break
        else:
            print("Please enter 1, 2, 3, or 4.\n")


"""Do not change anything below this line."""
if __name__ == "__main__":
    main()