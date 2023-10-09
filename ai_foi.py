# ai_foi.py 
# fighting_over_internships' AI for playing Wordle.
#
# Guess "SPARE" first, from there use collected data from guesses and feedback to decrease the size of the wordlist accordingly, 
# this goes for each time we have feedback returned and such after list size is adjusted to account for current possible values, 
# choose a random word from the remaining list and continue

import pdb
import random
import utils

def wordPurge(wordlist, guesses, feedback):
    count = 0 
    guess = guesses[len(guesses) - 1].upper()

    while (count < len(wordlist)): # while there is a word in the word list you have not gone over
        # initializes some booleans for if the word should be deleted and a false alarm
        deleted = False
        false_alarm = False
        word = wordlist[count].upper()
        
        if word == guess: # if the current word being looped through is the actual guess
            del wordlist[count]
            deleted = True
            continue
                
        for j in range(5): # loop over letters from current word in guess. We do this to check the value of feedback[i][j]
            if feedback[len(guesses) - 1][j] == 0: # GREY letter
                total_copy = word.count(guess[j])
                # If there aren't any copies of the letter being looked at in the current word from wordlist
                # just continue on to the next letter
                if total_copy == 0:
                    continue
                # Otherwise, check through the word and make sure it does not have more copies of the letter than there should be
                # there are some extra checks in this just to ensure that it doesn't remove more words than it should from wordlist
                else:
                    greens_and_yellows = 0
                    for k in range(5):
                        if guess[k] == guess[j]:
                            if feedback[len(guesses) - 1][k] > 0:
                                false_alarm = True
                                greens_and_yellows += 1
                    if not false_alarm:
                        del wordlist[count]
                        deleted = True
                        break
                    elif not (total_copy == greens_and_yellows):
                        del wordlist[count]
                        deleted = True
                        break
                    else:
                        continue
            elif feedback[len(guesses) - 1][j] == 1: # YELLOW letter
                if word.count(guess[j]) == 0: # check how many times the current letter appears in the word. If none, the word is invalid therefore delet
                    del wordlist[count]
                    deleted = True
                    break
                else:
                    for k in range(5): # Loop over letters in k
                        if k == j and word[k] == guess[j]: # if the letter at the shown index of each word is the same, check if the index is also the same, 
                                                           # if so then delete the word from the wordlist
                            del wordlist[count]
                            deleted = True
                            break #
            else: # feedback[len(guesses - 1)][j] == 2; GREEN letter
                if word.find(guess[j]) == -1: # letter at index j of guess is not in the word, delete the word from the list
                    del wordlist[count]
                    deleted = True
                    break
                else: # The letter has been found but now we need to make sure it's in the right spot
                    beans = False # flag beans to find if the letter searched is in the correct index of the current word
                    for k in range(5): # Loop over letters in k
                        if k == j and word[k] == guess[j]: # if the letter at the shown index of each word is the same, check if the index is also the same, 
                                                           # if so then delete the word from the wordlist
                            beans = True
                            break 
                    if beans == False:
                        del wordlist[count]
                        deleted = True
                        break
            if deleted == True:
                break
        if not deleted:
            count += 1
    

def makeguess(wordlist, guesses=[], feedback=[]):
    """Guess a word from the available wordlist, (optionally) using feedback 
    from previous guesses.
    
    Parameters
    ----------
    wordlist : list of str
        A list of the valid word choices. The output must come from this list.
    guesses : list of str
        A list of the previously guessed words, in the order they were made, 
        e.g. guesses[0] = first guess, guesses[1] = second guess. The length 
        of the list equals the number of guesses made so far. An empty list 
        (default) implies no guesses have been made.
    feedback : list of lists of int
        A list comprising one list per word guess and one integer per letter 
        in that word, to indicate if the letter is correct (2), almost 
        correct (1), or incorrect (0). An empty list (default) implies no 
        guesses have been made.
    Output
    ------
    word : str
        The word chosen by the AI for the next guess.
    """

    flag = False
    
    # makes the first guess SPARE
    if len(guesses) == 0:
        return "SPARE" # guess "SPARE" first because it has some really common letters in it and is a good place to start
    elif len(guesses) == 1: # Loop through feedback for the irate guess, if all feedback indexes are 0 (irate only returned grey letters) guess "CLOUD"
        for w in range(5): # if there are any green or yellow letters set the flag to true
            if feedback[0][w] == 1 or feedback[0][w] == 2: 
                flag = True
        if not flag: # if there are no yellow or green letters set the next choice to CLOUD 
                     # We cannot just return CLOUD because we still need to remove the words with the invalid letters from "IRATE"
            wordPurge(wordlist, guesses, feedback)
            return "CLOUD"
    elif len(guesses) == 2: # Loop through feedback for the irate guess, if all feedback indexes are 0 (irate only returned grey letters) guess "THINK"
                            # The same thing about cloud mentioned previously can be said here, we still want to remove invalid words
        for w in range(5): # if there are any green or yellow letters set the flag to true
            if feedback[0][w] == 1 or feedback[0][w] == 2 or feedback[1][w] == 1 or feedback[1][w] == 2: 
                flag = True
        if not flag: # if there are no yellow or green letters set the next choice to THINK
            wordPurge(wordlist, guesses, feedback)
            return "THINK"
    wordPurge(wordlist, guesses, feedback)
    return random.choice(wordlist)


if __name__ == "__main__":
    wordlist = utils.readwords("allwords5.txt")
    print(f"AI: 'My next choice would be {makeguess(wordlist)}'")
