''''
Job Wohali

DESCRIPTION:
My program checks a user inputted word against a list of "known" words. 
If the word the user is trying to spell is found, the program will 
show the user the correct spelling. If the word cannot be found in
our extensive list, the user will be asked if he wishes to add his 
word to the dictionary list. This, however, is really only helpful if the 
user is certain of the word's spelling; of course, you surely see the 
logical error with such being the case in a spell check program.
Albeit, I send you off, without further ado; have fun!
'''


######### reads the word list file & adds it to a list variable, "word_list"   #########
file = open("Spell_Checker/word_list.txt", "r")


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

##### set low and high index variables #####
list_length = len(word_list) - 1 #-1 because lists start on 0
low_idx = 0 #this will always start at 0
high_idx = list_length #this must be thus as the list will change size whenever you add to dictionary


######## looks for the user inputted word in the dictionary #######

#user_word is the word the user wants to check
user_word = input("What word would you like to check? ")

exit_loop = False #we'll use this later to exit first while loop and stop the program
exit_loop_2 = False #we'll use this to exit the second while loop

while low_idx <= high_idx and exit_loop == False: #this is while loop 1
    #establishes the mid index as midway point between first and last word
    mid_idx = int((low_idx + high_idx) / 2)
    #suggests the mid point word
    suggested_word = word_list[mid_idx]
                # print(f"suggested word position is ", word_list.index(suggested_word))
                # print(f"suggested word is {suggested_word}") #only fort troubleshooting. delete later

    #if the suggested word is correct, the PC lets the user know
    if suggested_word == user_word:
        print(f"'{suggested_word}' is the correct spelling!")
        print(f"Your word was found at position {mid_idx}.")
        exit_loop = True
        break

    #if the word is farther in the list than the suggested word, the program will look in the farther half
    elif user_word > suggested_word:
        low_idx = mid_idx + 1
    
    #if the word is earlier in the list than the suggested word, the program will look in the earlier half
    else: high_idx = mid_idx - 1

    if (high_idx - low_idx) == -1:
        word_not_found = True
        exit_loop = True
    
###### when the word is not in the list, tries to find the closest match ######

while not exit_loop_2 and suggested_word != user_word: #this is while loop 2
    low_idx_check = input(f"Did you mean {word_list[low_idx]}? (y/n)   ") #suggests the low index as a possibility
    if low_idx_check == "y":
        print(f"Nice! The word is spelled {word_list[low_idx]}") #confirms your word's spelling
        exit_loop_2 = True
    elif low_idx_check == "n":
        while True: #user proofs the high_idx_check
            high_idx_check = input(f"Did you mean {word_list[high_idx]}? (y/n)  ") #suggests high index as possibility
            if high_idx_check == "y":
                print(f"Nice! The word is spelled {word_list[high_idx]}") #confirms your word's spelling
                exit_loop_2 = True
                break  
            elif high_idx_check == 'n':
                while True: #user proofs "add_to_dictionary"
                    add_to_dictionary = input(f"Would you like to add {user_word} to the dictionary? (y/n)   ")
                   
                    ##########    block for adding to dictionary     ############ 
                    if add_to_dictionary == "y":
                        print(f"aiight, {user_word} is now in the dictionary.\nAnything else you need, feel free to run the program again!") 
                        file = open("Spell_Checker/word_list.txt", "w") #opens the file in write mode
                        for word in word_list:
                            file.write(f'{word}\n') #writes in all the words in our list
                        file.write(f'{user_word}\n') #allllso writes in our new word
                        file.close() #closes file

                        #####  now we sort the text list
                        file = open("Spell_Checker/word_list.txt", "r") #opens file in read mode
                        lines = file.readlines() #finds list of lines
                        file.close() #close file

                        lines.sort() #sorts said lines

                        file = open("Spell_Checker/word_list.txt", "w") #opens again in write mode
                        file.writelines(lines) #writes aforementioned lines to the file
                        file.close() #close file
                        exit_loop_2 = True #breaks out of second loop, ending program
                        break 
                    elif add_to_dictionary == "n":
                        exit_loop_2 = True #breaks out of second loop, ending program
                        break
                    else:
                        print(f"\ninvalid input. please enter y or n") #user proofing
                exit_loop_2 = True #breaks out of second loop, ending program
                break
            else:
                    print(f"\ninvalid input. please enter y or n") #user proofing

    #if the user doesn't answer y/n. more user proofing
    else:
        print(f"\ninvalid input. please enter y or n")
