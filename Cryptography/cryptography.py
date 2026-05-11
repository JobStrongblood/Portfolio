''''
Job Wohali

Description:
This program decrypts Ceasar Ciphers and encrypts text into Ceasar Cipher, with the shift key 
of the user's choice. While decrypting, if the shift key is unknown, the program will guide
the user through brute force finding the shift key. It will also tell the user what the shift
key is, once it is known.
'''

#set of symbols which the ciphers are based off of:
symbols = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890 '!?."

while True: #loop needed incase user enters invalid input into "mode"
    #uses either encrypt or decrypt functionality
    mode = input(f"\nDo you want to encrypt or decrypt? (enter 'e' or 'd') ")

    #code block for encrypting. Shifts the symbol set to the right
    if mode == "e":
        shift_question = input(f"\nWhat shift key do you want to use (Answer with an integer)? ")
        shift_key = int(shift_question) #names the shift key as an int
        plain_text = input(f"\nWhat do you want to encrypt? ") #user entry for text to be encrypted
        cipher_text = "" #creates cipher_text string but leaves it empty. Will assign value later.
        for char in plain_text:

            #find letter in our alphabet
            position = symbols.find(char)

            #if not found
            if position == -1:
                cipher_text += char

            #perform encrption
            encrypt_position = position + shift_key 
            encrypt_position = encrypt_position % len(symbols) #prevents the shift key from pushing position past string length
            cipher_text += symbols[encrypt_position] #shifts the plain text by the shift key amount
        
        #final cipher text result
        print(f"\nYour cipher text is ", cipher_text)
        break

    #code block for decrypting. Shifts the symbol set to the left
    if mode == "d":
        #prompts user for shift key
        shift_question = input(f"\nDo you know the shift key? (answer y/n) ")

        #if the user inputs "y"
        if shift_question == "y":
            shift_key = int(input(f"\nWhat is it? (answer with an integer) ")) #names the shift key as an int
        
        #if the user inputs anything other than "y", to upgrade make an elif for "n"
        else:
            shift_key = 1 #starts brute force decryption at shift = 1
            print("\nThen let's brute force this.")
        cipher_text = input(f"\nWhat do you want to decrypt? ") #user entry for text to be decrypted
        plain_text = "" #creates the plain_text string but leaves it empty. Will give it value later.

        ''''
        while True loop needed to print the entirety of plain_text, while being 
        able to repeat the process with the "Is this readable?" input.
        '''
        while True:
            #searches all characters in cipher_text 
            for char in cipher_text:

                # find the position of the character in our symbol set
                position = symbols.find(char)

                #if not found
                if position == -1:
                    plain_text += char

                #perform encryption 
                else:
                    decrypt_position = position - shift_key
                    decrypt_position = decrypt_position % len(symbols) #prevents the shift key from pushing position past string length
                    plain_text += symbols[decrypt_position] #shifts the cipher text by the shift key amount
            
            #prompts the user to see if brute force method has solved the cipher 
            readable = input(f"\n {plain_text}: Is this readable? (answer y/n) ")

            #if the user inputs 'y', indicating the cipher was solved
            if readable == "y":
                print("\nCongrats, your message is: ", plain_text)
                print("shift key = ", shift_key)
                break

            #if the user inputs 'n', indicating the output is simply nonsemse -_- 
            if readable == "n": #tries solving again, shifting the shift key up 1
                plain_text = ""
                shift_key += 1

            #if the user doesn't input 'y' or 'n', i.e. they put in some invalid input
            else:
                plain_text = "" #empties the plain text so it doesn't print the code twice. very neccesary 
                print("Input invalid. Try again.")
        break #ends the while True loop once the user has the end result they want

    else: #if the user doesn't enter "e" or "d" for the mode input 
        print("Input invalid, please try again.")
