'''
Job Strongblood Wohali

Program Description:
    Classic Hangman game. Guides the user through guessing
    a secret word by allowing the user to guess ONE letter 
    at a time. When the guessed letter is in the word, the 
    program will reveal to the user its correct position. 
    When the guessed letter is not in the word, it will 
    draw one body part of a stick man at a time. When the 
    stickman is fully drawn ("hanged"), the user has lost.
    The user's objective is to guess the word before this 
    happens. This will happen after 6 incorrect guesses.      
'''

import random
import os

'''
Function 1: Read Words 
Description: Opens a .txt file and writes it to a list
Parameter: The name of the file the user wants to open
Return Value: word_list (the text file in list variable form)
'''
def read_words(file_name):
    file = open(file_name, "r") #read only mode
    word_list = [] #creates the list variable
    end_file = False 

    while not end_file:
        #read from file
        word = file.readline()

        #reach end of file
        if word == "": #basically, if there is no word (ie value is nothing)
            end_file = True #stops writing to the list
        else:
            word = word.strip("\n") #take off the new line character
            word_list.append(word) #add to list

    file.close()
    return word_list

'''
Function 2: Random Select
Description: Randomly selects a word from a .txt file, using the read_words function
Parameter: NA
Return Value: secret_word, the above mentioned random word
'''
def rand_sel():
    words = read_words("Hangman/word_list.txt")
    secret_word = random.choice(words)
    #print(secret_word) #for debugging only -- reveals the answer
    return secret_word

'''
Function 3: Draw Hangman
Description: Clears the terminal before running, giving a clean UI. 
    Draws the gallows with word "H A N G M A N" overtop.
    Updates the stick-man per amount of missed guesses.
Parameters: misses - number of INCORRECT letter guesses
    used - number of total letters guessed
Return Value: None; only prints game UI
'''
def draw_hang(misses, used): #used is given a value of 0 WHEN there are no letters used
    os.system("clear") #note to user: may not work on Windows systems. Clears terminal before drawing hangman
    print("H A N G M A N")
    if misses == 0:
        print("_________")
        print("|/  	|")
        print("|       ")
        print("|      ")
        print("|_____ ")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 1:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|      ")
        print("|_____ ")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 2:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|       |")
        print("|_____ ")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 3:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|      /|")
        print("|_____ ")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 4:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|      /|\\")
        print("|_____ ")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 5:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|      /|\\")
        print("|_____ /")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
    elif misses == 6:
        print("_________")
        print("|/  	|")
        print("|       O")
        print("|      /|\\")
        print("|_____ / \\")
        print("|__________|")
        if used != 0: #used is given a value of 0 WHEN there are no letters used
            print(f"Letters guessed: {used}")
        print(f"\nSorry bub; you're out.")

'''
Function 4: Hide Word
Description: Converts the secret word to underscores; as the
    user guesses the word, function reveals it letter by letter
Parameters: hidden_word - string which will contain the underscores
    secret_word - word chosen randomly from word list
    right_guess - the user's letter guess
Return Value:hidden_word (updated with correct number of letters revealed)
'''
def hide_word(hidden_word, secret_word, right_guess): #right_guess is given a value of 0 WHEN there are no guesses yet made
    if right_guess != 0: #right_guess is given a value of 0 WHEN there are no guesses yet made
        for position, letter in enumerate(secret_word):
            if letter == right_guess:
                hidden_word[position] = right_guess #replaces the appropriate underscore with the right guess 
    for underscore in hidden_word:
        print(underscore, end=" ") # end=" " makes it print a space after each _, rather than put it on a new line
    return hidden_word 

'''
Function 5: Write Used Letter List
Description: Places all guessed letters into a list so that the 
    program can block the user from guessing the same letter twice
Parameter: None
Return Value: letter_list
'''
def write_used_letter_list():
    letter_list = []
    return letter_list

'''
Function 6: Game Loop
Description: Main game process, including accepting user input and 
    adjusting game based off of that input. Plays the game of hangman
    and is "user proofed", rejecting invalid entries without breaking the
    program. Includes win and lose conditions.
Parameter: The name of the file the user wants to open
Return Value: word_list (the text file in list variable form)
'''
def game_loop():
    print(f"Let's play some hangman!")
    hidden_word = []
    secret_word = rand_sel()
    used_letter_list = write_used_letter_list()
    miss_counter = 0
    for char in secret_word:
        hidden_word.append(f"_")
    draw_hang(miss_counter, 0)
    hide_word(hidden_word, secret_word, 0) #3rd parameter given a value of 0 since there are no letters yet guessed
    while True:
        user_guess = input(f"\Enter a LOWERCASE letter: ")
        if len(user_guess) == 1 and user_guess.isalpha() and user_guess not in used_letter_list:
            if str(user_guess) in str(secret_word):
                used_letter_list.append(user_guess)
                draw_hang(miss_counter, used_letter_list)
                print(f"\n{user_guess} is in the word \n")
                hide_word(hidden_word, secret_word, user_guess)
                if "_" not in hidden_word: #there will be no more _s once the word is totally revealed
                    print(f"\nYou won! I'm so proud. I knew you could!!!")
                    break #exits game loop, ending program
            else:
                used_letter_list.append(user_guess)
                miss_counter += 1
                draw_hang(miss_counter, used_letter_list)
                print(f"{user_guess} is not in the word")
                if miss_counter < 6: #this looks a little cleaner, not displaying the hidden word AGAIN once you've already lost
                    hide_word(hidden_word, secret_word, 0) #3rd parameter given a value of 0 since there are no letters yet guessed
                if miss_counter == 6:
                    print(f"Your word was {secret_word}.")
                    break #exits game loop, ending program
        else:
            print(f"\ninvalid input or letter already used, try again...")

#calls game loop function. All other functions are called within the other functions.    
game_loop()
